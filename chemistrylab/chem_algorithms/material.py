import inspect
import numpy as np
import math
import sys


class Material:
    def __init__(self,
                 name=None,
                 density=None,
                 polarity=None,
                 temperature=None,
                 pressure=None,
                 phase=None,
                 charge=None,
                 molar_mass=None,
                 color=None,
                 solute=False,
                 solvent=False,
                 boiling_point=None,
                 melting_point=None,
                 specific_heat=None,
                 enthalpy_fusion=None,
                 enthalpy_vapor=None,
                 index=None
                 ):
        self._name = name
        self.w2v = None  # not used
        self._density = density  # g/mL
        self._polarity = polarity
        self._temperature = temperature  # K
        self._pressure = pressure  # kPa
        self._phase = phase
        self._charge = charge
        self._molar_mass = molar_mass  # g/mol
        self._color = color
        self._solute = solute
        self._solvent = solvent
        self._boiling_point = boiling_point
        self._melting_point = melting_point
        self._specific_heat = specific_heat  # J/g*K
        self._enthalpy_fusion = enthalpy_fusion  # J/mol
        self._enthalpy_vapor = enthalpy_vapor  # J/mol
        self._index = index

    def _update_properties(self,
                           # temperature,
                           # pressure,
                           # polarity,
                           # density,
                           # phase,
                           ):
        feedback = []
        # called by event functions
        # update the rest of properties
        # check if any feedback is generated, if so feedback.append(['event', parameter])
        # return feedback
        return feedback

    # event functions
    def update_temperature(self, target_temperature, dt):  # this is an example
        feedback = []

        # update the material's temperature based on the target_temperature and dt
        # check if a feedback is generated
        # if generated, current_feedback.append(['feedback_event', parameter])
        # if target is not reached re-append this event to feedback

        feedback.extend(self._update_properties())
        return feedback

    def dissolve(self):
        # should be able to return how this material is dissolved
        # for NaCl this should at least return Na(charge=1) and Cl(charge=-1)
        # for the rest, like how Na and Cl dissolve in solvent, can be handled by the vessel's dissolve function
        pass

    # functions to access material's properties
    def get_name(self):
        return self._name

    def get_density(self):
        return self._density

    def get_polarity(self):
        return self._polarity

    def get_temperature(self):
        return self._temperature

    def get_pressure(self):
        return self._pressure

    def get_phase(self):
        return self._phase

    def get_charge(self):
        return self._charge

    def get_molar_mass(self):
        return self._molar_mass

    def get_color(self):
        return self._color

    def is_solute(self):
        return self._solute

    def is_solvent(self):
        return self._solvent

    def get_boiling_point(self, in_kelvin=False):
        temp = self._boiling_point

        if in_kelvin:
            temp = temp + 273.15

        return temp

    def get_melting_point(self, in_kelvin=False):
        temp = self._melting_point

        if in_kelvin:
            temp = temp + 273.15

        return temp

    # functions to change material's properties
    def set_solute_flag(self,
                        flag,
                        ):
        if flag:
            self._solute = True
            self._solvent = False
        elif not flag:
            self._solute = False

    def set_solvent_flag(self,
                         flag,
                         ):
        if flag:
            self._solvent = True
            self._solute = False
        elif not flag:
            self._solvent = False

    def set_charge(self,
                   charge):
        self._charge = charge

    def set_polarity(self,
                     polarity):
        self._polarity = polarity

    def set_specific_heat(self, specific_heat):
        self._specific_heat = specific_heat

    def set_enthalpy_fusion(self, enthalpy_fusion):
        self._enthalpy_fusion = enthalpy_fusion

    def set_enthalpy_vapor(self, enthalpy_vapor):
        self._enthalpy_vapor = enthalpy_vapor

    def get_index(self):
        return self._index


class Air(Material):
    def __init__(self):
        super().__init__(name='Air',
                         density=1.225e-3,  # in g/cm^3
                         temperature=297,  # in K
                         pressure=1,
                         phase='g',
                         molar_mass=28.963,  # in g/mol
                         color=0.65,
                         specific_heat=1.0035,  # in J/g*K
                         index=0
                         )


class H2O(Material):
    def __init__(self):
        super().__init__(name='H2O',
                         density=0.997,
                         polarity=abs(2 * 1.24 * np.cos((109.5 / 2) * (np.pi / 180.0))),
                         temperature=298,
                         pressure=1,
                         phase='l',
                         molar_mass=18.015,
                         color=0.2,
                         charge=0.0,
                         solute=False,
                         solvent=True,
                         specific_heat=4.1813,
                         index=1
                         )


class H(Material):
    def __init__(self):
        super().__init__(name='H',
                         density=8.9e-5,
                         polarity=0,
                         temperature=298,
                         pressure=1,
                         phase='g',
                         molar_mass=1.008,
                         color=0.1,
                         charge=0.0,
                         specific_heat=None,
                         index=2
                         )


class H2(Material):
    def __init__(self):
        super().__init__(name='H2',
                         density=8.9e-5,
                         polarity=0,
                         temperature=298,
                         pressure=1,
                         phase='g',
                         molar_mass=2.016,
                         color=0.1,
                         charge=0.0,
                         specific_heat=None,
                         index=3
                         )


class O(Material):
    def __init__(self):
        super().__init__(name='O',
                         density=1.429e-3,
                         polarity=0,
                         temperature=298,
                         pressure=1,
                         phase='g',
                         molar_mass=15.999,
                         color=0.15,
                         charge=0.0,
                         specific_heat=None,
                         index=4
                         )


class O2(Material):
    def __init__(self):
        super().__init__(name='O2',
                         density=1.429e-3,
                         polarity=0,
                         temperature=298,
                         pressure=1,
                         phase='g',
                         molar_mass=31.999,
                         color=0.1,
                         charge=0.0,
                         specific_heat=None,
                         index=5
                         )


class O3(Material):
    def __init__(self):
        super().__init__(name='O3',
                         density=2.144e-3,
                         polarity=abs(1 + 2 * -1 * np.cos((116.8 / 2) * (np.pi / 180.0))),
                         temperature=298,
                         pressure=1,
                         phase='g',
                         molar_mass=47.998,
                         color=0.1,
                         charge=-1.0,
                         specific_heat=None,
                         index=6
                         )


class C6H14(Material):
    def __init__(self):
        super().__init__(name='C6H14',
                         density=0.655,
                         polarity=0.0,
                         temperature=298,
                         pressure=1,
                         phase='l',
                         molar_mass=86.175,
                         color=0.65,
                         charge=0.0,
                         solvent=True,
                         specific_heat=2.26,
                         index=7
                         )


class NaCl(Material):
    def __init__(self):
        super().__init__(name='NaCl',
                         density=2.165,
                         polarity=1.5,
                         temperature=298,
                         pressure=1,
                         phase='s',
                         molar_mass=58.443,
                         color=0.9,
                         charge=0.0,
                         boiling_point=1738.0,
                         specific_heat=0.853,
                         enthalpy_fusion=27950.0,
                         enthalpy_vapor=229700.0,
                         index=8
                         )


# Polarity is dependant on charge for atoms
class Na(Material):
    def __init__(self):
        super().__init__(name='Na',
                         density=0.968,
                         polarity=0.0,
                         temperature=298,
                         pressure=1,
                         phase='s',
                         molar_mass=22.990,
                         color=0.85,
                         charge=0.0,
                         solute=True,
                         boiling_point=1156.0,
                         specific_heat=1.23,
                         enthalpy_fusion=2600.0,
                         enthalpy_vapor=97700.0,
                         index=9
                         )


# Note: Cl is very unstable when not an aqueous ion
class Cl(Material):
    def __init__(self):
        super().__init__(name='Cl',
                         density=3.214e-3,
                         polarity=0.0,
                         temperature=298,
                         pressure=1,
                         phase='g',
                         molar_mass=35.453,
                         color=0.8,
                         charge=0.0,
                         solute=True,
                         specific_heat=0.48,
                         enthalpy_fusion=3200.0,
                         enthalpy_vapor=10200.0,
                         index=10
                         )


class Cl2(Material):
    def __init__(self):
        super().__init__(name='Cl2',
                         density=2.898e-3,
                         polarity=0.0,
                         temperature=298,
                         pressure=1,
                         phase='g',
                         molar_mass=70.906,
                         color=0.8,
                         charge=0.0,
                         specific_heat=1.0,
                         index=11
                         )


class LiF(Material):
    def __init__(self):
        super().__init__(name='LiF',
                         density=2.640,
                         polarity=1.5,
                         temperature=298,
                         pressure=1,
                         phase='s',
                         molar_mass=25.939,
                         color=0.9,
                         charge=0.0,
                         specific_heat=1.0,
                         index=12
                         )


class Li(Material):
    def __init__(self):
        super().__init__(name='Li',
                         density=0.534,
                         polarity=0.0,
                         temperature=298,
                         pressure=1,
                         phase='s',
                         molar_mass=6.941,
                         color=0.95,
                         charge=0.0,
                         specific_heat=1.0,
                         index=13
                         )


# Note: F is very unstable when not an aqueous ion
class F(Material):
    def __init__(self):
        super().__init__(name='F',
                         density=1.696e-3,
                         polarity=0.0,
                         temperature=298,
                         pressure=1,
                         phase='g',
                         molar_mass=18.998,
                         color=0.8,
                         charge=0.0,
                         specific_heat=None,
                         index=14
                         )


class F2(Material):
    def __init__(self):
        super().__init__(name='F2',
                         density=1.696e-3,
                         polarity=0.0,
                         temperature=298,
                         pressure=1,
                         phase='g',
                         molar_mass=37.997,
                         color=0.8,
                         charge=0.0,
                         specific_heat=None,
                         index=15
                         )


## ---------- ## HYDROCARBONS ## ---------- ##


class Dodecane(Material):
    def __init__(self):
        super().__init__(
            name='dodecane',
            density=0.75,
            polarity=0.0,
            temperature=298,
            pressure=1,
            phase='l',
            molar_mass=170.34,
            color=0.05,
            charge=0.0,
            boiling_point=489.5,
            melting_point=263.6,
            solute=False,
            specific_heat=2.3889,  # in J/g*K
            enthalpy_fusion=19790.0,
            enthalpy_vapor=41530.0,
            index=16
        )


class OneChlorohexane(Material):
    def __init__(self):
        super().__init__(
            name='1-chlorohexane',
            density=0.879,
            polarity=0.0,
            temperature=298,
            pressure=1,
            phase='l',
            molar_mass=120.62,
            color=0.1,
            charge=0.0,
            boiling_point=408.2,
            melting_point=179.2,
            solute=False,
            specific_heat=1.5408,
            enthalpy_fusion=15490.0,
            enthalpy_vapor=42800.0,
            index=17
        )


class TwoChlorohexane(Material):
    def __init__(self):
        super().__init__(
            name='2-chlorohexane',
            density=0.87,
            polarity=0.0,
            temperature=298,
            pressure=1,
            phase='l',
            molar_mass=120.62,
            color=0.15,
            charge=0.0,
            boiling_point=395.2,
            melting_point=308.3,
            solute=False,
            specific_heat=1.5408,
            enthalpy_fusion=11970.0,
            enthalpy_vapor=43820.0,
            index=18
        )


class ThreeChlorohexane(Material):
    def __init__(self):
        super().__init__(
            name='3-chlorohexane',
            density=0.9,
            polarity=0.0,
            temperature=298,
            pressure=1,
            phase='l',
            molar_mass=120.62,
            color=0.2,
            charge=0.0,
            boiling_point=396.2,
            melting_point=308.3,
            solute=False,
            specific_heat=1.5408,
            enthalpy_fusion=11970.0,
            enthalpy_vapor=32950.0,
            index=19
        )


class FiveMethylundecane(Material):
    def __init__(self):
        super().__init__(
            name='5-methylundecane',
            density=0.75,
            polarity=0.0,
            temperature=298,
            pressure=1,
            phase='l',
            molar_mass=170.34,
            color=0.25,
            charge=0.0,
            boiling_point=481.1,
            melting_point=255.2,
            solute=False,
            specific_heat=2.3889,
            enthalpy_fusion=19790.0,
            enthalpy_vapor=41530.0,
            index=20
        )


class FourEthyldecane(Material):
    def __init__(self):
        super().__init__(
            name='4-ethyldecane',
            density=0.75,
            polarity=0.0,
            temperature=298,
            pressure=1,
            phase='l',
            molar_mass=170.34,
            color=0.3,
            charge=0.0,
            boiling_point=480.1,
            melting_point=254.2,
            solute=False,
            specific_heat=2.3889,
            enthalpy_fusion=19790.0,
            enthalpy_vapor=41530.0,
            index=21
        )


class FiveSixDimethyldecane(Material):
    def __init__(self):
        super().__init__(
            name='5,6-dimethyldecane',
            density=0.757,
            polarity=0.0,
            temperature=298,
            pressure=1,
            phase='l',
            molar_mass=170.34,
            color=0.35,
            charge=0.0,
            boiling_point=474.2,
            melting_point=222.4,
            solute=False,
            specific_heat=2.3889,
            enthalpy_fusion=19790.0,
            enthalpy_vapor=41530.0,
            index=22
        )


class FourEthylFiveMethylnonane(Material):
    def __init__(self):
        super().__init__(
            name='4-ethyl-5-methylnonane',
            density=0.75,
            polarity=0.0,
            temperature=298,
            pressure=1,
            phase='l',
            molar_mass=170.34,
            color=0.4,
            charge=0.0,
            boiling_point=476.3,
            melting_point=224.5,
            solute=False,
            specific_heat=2.3889,
            enthalpy_fusion=19790.0,
            enthalpy_vapor=41530.0,
            index=23
        )


class FourFiveDiethyloctane(Material):
    def __init__(self):
        super().__init__(
            name='4,5-diethyloctane',
            density=0.768,
            polarity=0.0,
            temperature=298,
            pressure=1,
            phase='l',
            molar_mass=170.34,
            color=0.45,
            charge=0.0,
            boiling_point=470.2,
            melting_point=222.4,
            solute=False,
            specific_heat=2.3889,
            enthalpy_fusion=19790.0,
            enthalpy_vapor=41530.0,
            index=24
        )


class Ethoxyethane(Material):
    def __init__(self):
        super().__init__(
            name='ethoxyethane',
            density=0.713,
            polarity=0.0,
            temperature=298,
            pressure=1,
            phase='l',
            molar_mass=74.123,
            color=0.5,
            charge=0.0,
            boiling_point=34.6,
            melting_point=-116.3,
            solute=False,
            solvent=True,
            specific_heat=2.253,
            enthalpy_fusion=7190.0,
            enthalpy_vapor=27250.0,
            index=25
        )


class EthylAcetate(Material):
    def __init__(self):
        super().__init__(
            name='ethyl acetate',
            density=0.902,
            polarity=0.654,
            temperature=298,
            pressure=1,
            phase='l',
            molar_mass=88.106,
            color=0.05,
            charge=0.0,
            boiling_point=350,
            melting_point=189.6,
            solvent=True,
            specific_heat=1.904,  # in J/g*K
            enthalpy_fusion=10480,
            enthalpy_vapor=31940,
            index=26
        )


class DiEthylEther(Material):
    def __init__(self):
        super().__init__(
            name='diethyl ether',
            density=0.7134,
            polarity=1.3,
            temperature=298,
            pressure=1,
            phase='l',
            molar_mass=74.123,
            color=0.05,
            charge=0.0,
            boiling_point=307.8,
            melting_point=156.8,
            solvent=True,
            specific_heat=119.46,  # in J/g*K
            enthalpy_fusion=-252.7e3,
            enthalpy_vapor=27.247e3,
            index=29
        )


##------Indicators------##


class MethylRed(Material):
    def __init__(self):
        super().__init__(
            name='methyl red',
            density=0.902,
            polarity=0.0,
            temperature=298,
            pressure=1,
            phase='s',
            molar_mass=88.106,
            color=0.6,
            charge=0.0,
            boiling_point=630,
            melting_point=455,
            solute=True,
            specific_heat=1.904,  # in J/g*K
            enthalpy_fusion=10480,
            enthalpy_vapor=31940,
            index=27
        )


##-------Acids-------##


class HCl(Material):
    def __init__(self):
        super().__init__(
            name='HCl',
            density=1.48e-3,
            polarity=0.0,
            temperature=298,
            pressure=1,
            phase='g',
            molar_mass=88.106,
            color=0.3,
            charge=0.0,
            boiling_point=350,
            melting_point=189.6,
            solute=True,
            specific_heat=1.904,  # in J/g*K
            enthalpy_fusion=10480,
            enthalpy_vapor=31940,
            index=28
        )


def get_materials():
    '''
    '''

    names_list = []
    objects_list = []
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if all([
            inspect.isclass(obj),
            name != "Material"
        ]):
            names_list.append(name)
            objects_list.append(obj)

    return (names_list, objects_list)


total_num_material = len(Material.__subclasses__())

#
#
# class T1(Material):
#     def __init__(self):
#         super().__init__(name='temp1',
#                          density=0.655,
#                          polarity=0.9,
#                          temperature=298,
#                          )
#
#
# class T2(Material):
#     def __init__(self):
#         super().__init__(name='temp2',
#                          density=0.655,
#                          polarity=0.1,
#                          temperature=298,
#                          )
