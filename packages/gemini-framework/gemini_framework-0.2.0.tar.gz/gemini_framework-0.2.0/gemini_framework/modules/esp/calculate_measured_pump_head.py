from gemini_framework.abstract.unit_module_abstract import UnitModuleAbstract
from gemini_model.pump.esp import ESP
import traceback


class CalculateMeasuredPumpHead(UnitModuleAbstract):

    def __init__(self, unit):
        super().__init__(unit)

        self.model = ESP()

        self.link_input('measured', 'esp_inlet_pressure')
        self.link_input('calculated', 'esp_discharge_pressure')
        self.link_output('calculated', 'esp_measured_head')

    def step(self, loop):
        self.loop = loop
        self.loop.start_time = self.get_output_last_data_time('esp_measured_head')
        self.loop.compute_n_simulation()

        time, esp_intake = self.get_input_data('esp_inlet_pressure')
        time, esp_discharge = self.get_input_data('esp_discharge_pressure')

        esp_measured_head = []
        time_calc = []
        for ii in range(1, self.loop.n_step + 1):
            try:
                esp_head = esp_discharge[ii] - esp_intake[ii]

                esp_measured_head.append(esp_head)
                time_calc.append(time[ii])
            except Exception:
                self.logger.warn(
                    "ERROR in module " + self.__class__.__name__ + " : " + traceback.format_exc())
                esp_measured_head.append(None)

        if time_calc:
            self.write_output_data('esp_measured_head', time_calc, esp_measured_head)
