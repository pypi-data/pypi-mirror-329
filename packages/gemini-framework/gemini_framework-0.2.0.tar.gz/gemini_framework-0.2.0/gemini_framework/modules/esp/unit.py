from gemini_framework.abstract.unit_abstract import UnitAbstract
from gemini_framework.modules.esp.calculate_theoretical_pump_head \
    import CalculateTheoreticalPumpHead
from gemini_framework.modules.esp.calculate_theoretical_pump_power \
    import CalculateTheoreticalPumpPower
from gemini_framework.modules.esp.calculate_pump_discharge_pressure \
    import CalculatePumpDischargePressure
from gemini_framework.modules.esp.calculate_measured_pump_head \
    import CalculateMeasuredPumpHead
from gemini_framework.modules.esp.calculate_pump_intake_pressure \
    import CalculatePumpIntakePressure


class ESPUnit(UnitAbstract):
    """A ESPUnit represents ESP modules."""

    def __init__(self, unit_id, unit_name, plant):
        super().__init__(unit_id=unit_id, unit_name=unit_name, plant=plant)

        # define unit modules
        self.modules['preprocessor'] = []
        self.modules['model'].append(CalculateTheoreticalPumpHead(self))
        self.modules['model'].append(CalculateTheoreticalPumpPower(self))
        self.modules['model'].append(CalculatePumpDischargePressure(self))
        self.modules['model'].append(CalculateMeasuredPumpHead(self))
        self.modules['model'].append(CalculatePumpIntakePressure(self))
        self.modules['postprocessor'] = []
