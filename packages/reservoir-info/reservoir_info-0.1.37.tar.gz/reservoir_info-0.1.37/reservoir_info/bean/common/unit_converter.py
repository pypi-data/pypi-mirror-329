from mag_tools.model.common.unit_system import UnitSystem

from model.unit_convert_factor import UnitConvertFactor
from model.unit_type import UnitType


class UnitConverter:
    __unit_map = {
        UnitSystem.METRIC: {
            UnitType.LENGTH: "m",
            UnitType.SURFACE_VOLUME_LIQ: "m³",
            UnitType.SURFACE_VOLUME_GAS: "m³",
            UnitType.SUBSURFACE_VOLUME: "m³",
            UnitType.DENSITY: "kg/m³",
            UnitType.PRESSURE: "bar",
            UnitType.TIME: "day",
            UnitType.ABS_TEMPERATURE: "°K",
            UnitType.REL_TEMPERATURE: "°C",
            UnitType.WI: "mD∙m",
            UnitType.TF: "cP∙m3/day/bar",
            UnitType.PERMEABILITY: "mD",
            UnitType.VISCOSITY: "cP",
            UnitType.SURFACE_TENSION: "mN/m",
            UnitType.FORCHHEIMER_BETA: "F"
        },
        UnitSystem.FIELD: {
            UnitType.LENGTH: "ft",
            UnitType.SURFACE_VOLUME_LIQ: "STB",
            UnitType.SURFACE_VOLUME_GAS: "Mscf",
            UnitType.SUBSURFACE_VOLUME: "ft³",
            UnitType.DENSITY: "lb/ft³",
            UnitType.PRESSURE: "psi",
            UnitType.TIME: "day",
            UnitType.ABS_TEMPERATURE: "°R",
            UnitType.REL_TEMPERATURE: "°F",
            UnitType.WI: "mD∙ft",
            UnitType.TF: "cP∙STB/day/psi",
            UnitType.PERMEABILITY: "mD",
            UnitType.VISCOSITY: "cP",
            UnitType.SURFACE_TENSION: "mN/m",
            UnitType.FORCHHEIMER_BETA: "F"
        },
        UnitSystem.LAB: {
            UnitType.LENGTH: "cm",
            UnitType.SURFACE_VOLUME_LIQ: "cm³",
            UnitType.SURFACE_VOLUME_GAS: "cm³",
            UnitType.SUBSURFACE_VOLUME: "cm³",
            UnitType.DENSITY: "g/cm³",
            UnitType.PRESSURE: "atm",
            UnitType.TIME: "hour",
            UnitType.ABS_TEMPERATURE: "°K",
            UnitType.REL_TEMPERATURE: "°C",
            UnitType.WI: "mD∙cm",
            UnitType.TF: "cP∙cm³/hour/atm",
            UnitType.PERMEABILITY: "mD",
            UnitType.VISCOSITY: "cP",
            UnitType.SURFACE_TENSION: "mN/m",
            UnitType.FORCHHEIMER_BETA: "F"
        },
        UnitSystem.MESO: {
            UnitType.LENGTH: "μm",
            UnitType.SURFACE_VOLUME_LIQ: "μm³",
            UnitType.SURFACE_VOLUME_GAS: "μm³",
            UnitType.SUBSURFACE_VOLUME: "μm³",
            UnitType.DENSITY: "pg/μm³",
            UnitType.PRESSURE: "Pa",
            UnitType.TIME: "ms",
            UnitType.ABS_TEMPERATURE: "°K",
            UnitType.REL_TEMPERATURE: "°F",
            UnitType.WI: "mD∙μm",
            UnitType.TF: "cP∙μm³/ms/Pa",
            UnitType.PERMEABILITY: "mD",
            UnitType.VISCOSITY: "cP",
            UnitType.SURFACE_TENSION: "mN/m",
            UnitType.FORCHHEIMER_BETA: "F"
        }
    }

    __conversion_factors = {
        UnitSystem.METRIC: {
            UnitConvertFactor.DARCY: 9.869233e-13,  # m²
            UnitConvertFactor.GRAVITY: 9.80665,  # m/s²
            UnitConvertFactor.FORCHHEIMER: 1.0,  # Placeholder value
            UnitConvertFactor.IDEAL_GAS_CONSTANT: 8.314,  # J/(mol·K)
        },
        UnitSystem.FIELD: {
            UnitConvertFactor.DARCY: 1.0,  # Darcy
            UnitConvertFactor.GRAVITY: 32.174,  # ft/s²
            UnitConvertFactor.FORCHHEIMER: 1.0,  # Placeholder value
            UnitConvertFactor.IDEAL_GAS_CONSTANT: 10.7316,  # ft³·psi/(lb·mol·R)
        },
        UnitSystem.LAB: {
            UnitConvertFactor.DARCY: 9.869233e-13,  # m²
            UnitConvertFactor.GRAVITY: 9.80665,  # m/s²
            UnitConvertFactor.FORCHHEIMER: 1.0,  # Placeholder value
            UnitConvertFactor.IDEAL_GAS_CONSTANT: 8.314,  # J/(mol·K)
        },
        UnitSystem.MESO: {
             UnitConvertFactor.DARCY: 9.869233e-13,  # m²
             UnitConvertFactor.GRAVITY: 9.80665,  # m/s²
             UnitConvertFactor.FORCHHEIMER: 1.0,  # Placeholder value
             UnitConvertFactor.IDEAL_GAS_CONSTANT: 8.314,  # J/(mol·K)
         }
    }

    @classmethod
    def get_unit(cls, system, unit_type):
        """
        根据单位制和单位类型返回相应的单位。

        参数：
        :param system: 单位制（如 UnitSystem.METRIC）
        :param unit_type: 单位类型（如 UnitType.LENGTH）
        :return: 对应的单位
        """
        return cls.__unit_map.get(system, {}).get(unit_type, "unknown")

    @classmethod
    def get_conversion_factor(cls, system, factor):
        """
        根据单位制和转换系数类型返回相应的转换系数。

        参数：
        :param system: 单位制（如 UnitSystem.METRIC）
        :param factor: 转换系数类型（如 UnitConvertFactor.DARCY）
        :return: 对应的转换系数
        """
        return cls.__conversion_factors.get(system, {}).get(factor, "unknown")
