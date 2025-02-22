from gemini_framework.abstract.unit_module_abstract import UnitModuleAbstract
from gemini_model.reservoir.inflow_performance import IPR
from gemini_model.well.pressure_drop import DPDT
from gemini_model.fluid.pvt_water_stp import PVTConstantSTP
from gemini_model.pump.esp import ESP
import numpy as np
import traceback


class CalculatePumpIntakePressure(UnitModuleAbstract):

    def __init__(self, unit):
        super().__init__(unit)

        self.model = ESP()
        self.VLP = DPDT()
        self.VLP.PVT = PVTConstantSTP()
        self.IPR = IPR()

        self.link_input('measured', 'esp_flow')
        self.link_output('calculated', 'esp_intake_pressure')

    def step(self, loop):
        self.loop = loop
        self.loop.start_time = self.get_output_last_data_time('esp_intake_pressure')
        self.loop.compute_n_simulation()

        time, esp_flow = self.get_input_data('esp_flow')  # m3/hr

        """Calculate bottomhole pressure from reservoir"""
        u = dict()

        pbh_res = []
        time_calc = []
        for ii in range(1, self.loop.n_step + 1):
            try:
                self.update_model_parameter(time[ii])

                u['flow'] = esp_flow[ii] / 3600  # convert to seconds

                x = []
                self.IPR.calculate_output(u, x)

                # ASSERT
                y = self.IPR.get_output()

                pbh_res.append(y['pressure_bottomhole'])
                time_calc.append(time[ii])
            except Exception as e:
                self.logger.warn("ERROR:" + repr(e))
                pbh_res.append(None)

        """Calculate pressure drop from bottomhole to ESP"""
        u = dict()

        intake_pressure = []
        time_calc = []
        for ii in range(1, self.loop.n_step + 1):
            try:
                self.update_model_parameter(time[ii])

                u['pressure'] = pbh_res[ii - 1] * 1e5
                u['temperature'] = self.IPR.parameters['reservoir_temperature'] + 273.15  # C to K
                u['flowrate'] = esp_flow[ii] / 3600  # m3/hr to m3/s
                u['temperature_ambient'] = self.VLP.parameters[
                                               'soil_temperature'] + 273.15  # C to K
                u['direction'] = 'up'

                x = []
                self.VLP.calculate_output(u, x)

                # ASSERT
                y = self.VLP.get_output()

                intake_pressure.append(y['pressure_output'] / 1e5)  # Pa to bar
                time_calc.append(time[ii])
            except Exception:
                self.logger.warn(
                    "ERROR in module " + self.__class__.__name__ + " : " + traceback.format_exc())
                intake_pressure.append(None)

        if time_calc:
            self.write_output_data('esp_intake_pressure', time_calc, intake_pressure)

    def update_model_parameter(self, timestamp):

        esp_unit = self.unit
        well_unit = self.unit.from_units[0]
        reservoir_unit = well_unit.from_units[0]

        esp_index = self.get_parameter_index(esp_unit, timestamp)
        well_index = self.get_parameter_index(well_unit, timestamp)
        reservoir_index = self.get_parameter_index(reservoir_unit, timestamp)

        well_param = dict()
        well_param['soil_temperature'] = well_unit.parameters['property'][well_index][
            'productionwell_soil_temperature']

        well_traj = well_unit.parameters['property'][well_index]['productionwell_trajectory_table']
        length = []
        diameter = []
        angle = []
        roughness = []
        for ii in range(1, len(well_traj)):
            if well_traj[ii - 1]['MD'] >= esp_unit.parameters['property'][esp_index]['esp_depth']:
                MD = well_traj[ii]['MD'] - well_traj[ii - 1]['MD']
                TVD = well_traj[ii]['TVD'] - well_traj[ii - 1]['TVD']

                length.append(MD)
                diameter.append(well_traj[ii]['ID'])
                angle.append(np.round(90 - np.arccos(TVD / MD) * 180 / np.pi, 2) * np.pi / 180)
                roughness.append(well_traj[ii]['roughness'])

        well_param['diameter'] = np.array(diameter)  # well diameter in [m]
        well_param['length'] = np.array(length)  # well depth in [m]
        well_param['angle'] = np.array(angle)  # well angle in [degree]
        well_param['roughness'] = roughness  # roughness of cells [m]
        well_param['friction_correlation'] = well_unit.parameters['property'][well_index][
            'productionwell_friction_correlation']

        self.VLP.update_parameters(well_param)

        pvt_param = dict()
        pvt_param['RHOL'] = reservoir_unit.parameters['property'][reservoir_index]['liquid_density']
        pvt_param['VISL'] = reservoir_unit.parameters['property'][reservoir_index][
            'liquid_viscosity']

        self.VLP.PVT.update_parameters(pvt_param)

        res_param = dict()
        res_param['reservoir_pressure'] = reservoir_unit.parameters['property'][reservoir_index][
            'reservoir_pressure']
        res_param['reservoir_temperature'] = reservoir_unit.parameters['property'][reservoir_index][
            'reservoir_temperature']
        res_param['productivity_index'] = well_unit.parameters['property'][well_index][
            'productionwell_productivity_index']
        res_param['type'] = 'production_reservoir'

        self.IPR.update_parameters(res_param)
