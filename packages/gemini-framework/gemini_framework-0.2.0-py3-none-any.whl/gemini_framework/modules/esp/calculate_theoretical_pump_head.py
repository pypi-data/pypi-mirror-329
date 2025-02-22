from gemini_framework.abstract.unit_module_abstract import UnitModuleAbstract
from gemini_model.pump.esp import ESP
import numpy as np
import traceback


class CalculateTheoreticalPumpHead(UnitModuleAbstract):

    def __init__(self, unit):
        super().__init__(unit)

        self.model = ESP()

        self.link_input('measured', 'esp_flow')
        self.link_input('measured', 'esp_frequency')
        self.link_output('calculated', 'esp_head')

    def step(self, loop):
        self.loop = loop
        self.loop.start_time = self.get_output_last_data_time('esp_head')
        self.loop.compute_n_simulation()

        time, esp_flow = self.get_input_data('esp_flow')
        time, esp_frequency = self.get_input_data('esp_frequency')

        u = dict()
        esp_pump_head = []
        time_calc = []
        for ii in range(1, self.loop.n_step + 1):
            try:
                self.update_model_parameter(time[ii])

                u['pump_flow'] = esp_flow[ii] / 3600  # convert to seconds
                u['pump_freq'] = esp_frequency[ii]

                x = []
                self.model.calculate_output(u, x)

                y = self.model.get_output()

                esp_pump_head.append(y['pump_head'] / 1e5)  # convert to bar
                time_calc.append(time[ii])
            except Exception:
                self.logger.warn(
                    "ERROR in module " + self.__class__.__name__ + " : " + traceback.format_exc())
                esp_pump_head.append(None)

        if time_calc:
            self.write_output_data('esp_head', time_calc, esp_pump_head)

    def update_model_parameter(self, timestamp):

        index = self.get_parameter_index(self.unit, timestamp)

        esp_param = dict()
        esp_param['no_stages'] = self.unit.parameters['property'][index]['esp_no_stage']
        esp_param['pump_name'] = self.unit.parameters['property'][index]['esp_type']
        esp_param['head_coeff'] = np.asarray(self.unit.parameters['property'][index]
                                             ['esp_head_coeff'].split(';'), dtype=np.float32)
        esp_param['power_coeff'] = np.asarray(self.unit.parameters['property'][index]
                                              ['esp_power_coeff'].split(';'), dtype=np.float32)

        self.model.update_parameters(esp_param)
