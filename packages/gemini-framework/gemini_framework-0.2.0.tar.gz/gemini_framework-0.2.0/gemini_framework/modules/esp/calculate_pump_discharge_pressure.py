from gemini_framework.abstract.unit_module_abstract import UnitModuleAbstract
from gemini_model.well.pressure_drop import DPDT
from gemini_model.fluid.pvt_water_stp import PVTConstantSTP
from gemini_model.pump.esp import ESP
import numpy as np
import traceback


class CalculatePumpDischargePressure(UnitModuleAbstract):

    def __init__(self, unit):
        super().__init__(unit)

        self.model = ESP()
        self.VLP1 = DPDT()
        self.VLP1.PVT = PVTConstantSTP()

        self.link_input('measured', 'esp_flow')
        self.link_output('calculated', 'esp_discharge_pressure')

    def step(self, loop):
        self.loop = loop
        self.loop.start_time = self.get_output_last_data_time('esp_discharge_pressure')
        self.loop.compute_n_simulation()

        well_unit = self.unit.from_units[0]

        # Get well data
        database = None
        for database in self.unit.plant.databases:
            if database.category == 'measured':
                break

        wellhead_pressure, time = database.read_internal_database(
            self.unit.plant.name,
            well_unit.name,
            'productionwell_wellhead_pressure.measured',
            self.loop.start_time,
            self.loop.end_time,
            str(self.loop.timestep) + 's'
        )

        wellhead_temperature, time = database.read_internal_database(
            self.unit.plant.name,
            well_unit.name,
            'productionwell_wellhead_temperature.measured',
            self.loop.start_time,
            self.loop.end_time,
            str(self.loop.timestep) + 's'
        )

        time, well_flow = self.get_input_data('esp_flow')

        """Calculate discharge pressure via the pressure dop from wellhead to ESP"""
        u = dict()
        discharge_pressure = []
        time_calc = []
        for ii in range(1, self.loop.n_step + 1):
            try:
                self.update_model_parameter(time[ii])

                u['pressure'] = wellhead_pressure[ii] * 1e5  # bar to Pa
                u['temperature'] = wellhead_temperature[ii] + 273.15  # C to K
                u['flowrate'] = well_flow[ii] / 3600  # m3/hr to m3/s
                u['temperature_ambient'] = self.VLP1.parameters[
                                               'soil_temperature'] + 273.15  # C to K
                u['direction'] = 'down'

                x = []
                self.VLP1.calculate_output(u, x)

                # ASSERT
                y = self.VLP1.get_output()

                discharge_pressure.append(y['pressure_output'] / 1e5)  # Pa to bar
                time_calc.append(time[ii])
            except Exception:
                self.logger.warn(
                    "ERROR in module " + self.__class__.__name__ + " : " + traceback.format_exc())
                discharge_pressure.append(None)

        if time_calc:
            self.write_output_data('esp_discharge_pressure', time_calc, discharge_pressure)

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

        well_param['diameter'] = np.array(
            [esp_unit.parameters['property'][esp_index]['esp_tubing']])  # well diameter in [m]
        well_param['length'] = np.array(
            [esp_unit.parameters['property'][esp_index]['esp_depth']])  # well depth in [m]
        well_param['angle'] = np.array([90 * np.pi / 180])  # well angle in [degree]
        well_traj = well_unit.parameters['property'][well_index]['productionwell_trajectory_table']
        well_param['roughness'] = np.array(
            [well_traj[1]['roughness']])  # roughness of cells [m]
        well_param['friction_correlation'] = well_unit.parameters['property'][well_index][
            'productionwell_friction_correlation']

        self.VLP1.update_parameters(well_param)

        pvt_param = dict()
        pvt_param['RHOL'] = reservoir_unit.parameters['property'][reservoir_index]['liquid_density']
        pvt_param['VISL'] = reservoir_unit.parameters['property'][reservoir_index][
            'liquid_viscosity']

        self.VLP1.PVT.update_parameters(pvt_param)
