"""
Trossen Arm Python Bindings
"""
from __future__ import annotations
import pybind11_stubgen.typing_ext
import typing
__all__ = ['EndEffectorProperties', 'IPMethod', 'LinkProperties', 'Mode', 'Model', 'StandardEndEffector', 'TrossenArmDriver']
class EndEffectorProperties:
    """
    @brief End effector properties
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self) -> None:
        ...
    @property
    def finger_left(self) -> LinkProperties:
        """
                @brief Properties of the left finger link
        """
    @finger_left.setter
    def finger_left(self, arg0: LinkProperties) -> None:
        ...
    @property
    def finger_right(self) -> LinkProperties:
        """
                @brief Properties of the right finger link
        """
    @finger_right.setter
    def finger_right(self, arg0: LinkProperties) -> None:
        ...
    @property
    def offset_finger_left(self) -> float:
        """
                @brief Offset from the palm center to the left carriage center in m in home configuration
        """
    @offset_finger_left.setter
    def offset_finger_left(self, arg0: float) -> None:
        ...
    @property
    def offset_finger_right(self) -> float:
        """
                @brief Offset from the palm center to the right carriage center in m in home configuration
        """
    @offset_finger_right.setter
    def offset_finger_right(self, arg0: float) -> None:
        ...
    @property
    def palm(self) -> LinkProperties:
        """
                @brief Properties of the palm link
        """
    @palm.setter
    def palm(self, arg0: LinkProperties) -> None:
        ...
class IPMethod:
    """
    @brief IP methods
    
    Members:
    
      manual : 
            @brief Manual: use the manual IP address specified in the configuration
          
    
      dhcp : 
            @brief DHCP: use the DHCP to obtain the IP address, if failed,
              use the default IP address
          
    """
    __members__: typing.ClassVar[dict[str, IPMethod]]  # value = {'manual': <IPMethod.manual: 0>, 'dhcp': <IPMethod.dhcp: 1>}
    dhcp: typing.ClassVar[IPMethod]  # value = <IPMethod.dhcp: 1>
    manual: typing.ClassVar[IPMethod]  # value = <IPMethod.manual: 0>
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class LinkProperties:
    """
    @brief Link properties
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self) -> None:
        ...
    @property
    def inertia(self) -> typing.Annotated[list[float], pybind11_stubgen.typing_ext.FixedSize(9)]:
        """
                @brief inertia in kg m^2
        """
    @inertia.setter
    def inertia(self, arg0: typing.Annotated[list[float], pybind11_stubgen.typing_ext.FixedSize(9)]) -> None:
        ...
    @property
    def mass(self) -> float:
        """
                @brief mass in kg
        """
    @mass.setter
    def mass(self, arg0: float) -> None:
        ...
    @property
    def origin_rpy(self) -> typing.Annotated[list[float], pybind11_stubgen.typing_ext.FixedSize(3)]:
        """
                @brief inertia frame RPY angles measured in link frame in rad
        """
    @origin_rpy.setter
    def origin_rpy(self, arg0: typing.Annotated[list[float], pybind11_stubgen.typing_ext.FixedSize(3)]) -> None:
        ...
    @property
    def origin_xyz(self) -> typing.Annotated[list[float], pybind11_stubgen.typing_ext.FixedSize(3)]:
        """
                @brief inertia frame translation measured in link frame in m
        """
    @origin_xyz.setter
    def origin_xyz(self, arg0: typing.Annotated[list[float], pybind11_stubgen.typing_ext.FixedSize(3)]) -> None:
        ...
class Mode:
    """
    @brief Operation modes of a joint
    
    Members:
    
      idle : 
            @brief Idle mode: arm joints are braked, the gripper joint closing with a safe force
          
    
      position : 
            @brief Position mode: control the joint to a desired position
          
    
      velocity : 
            @brief Velocity mode: control the joint to a desired velocity
          
    
      effort : 
            @brief Effort mode: control the joint to a desired effort
          
    """
    __members__: typing.ClassVar[dict[str, Mode]]  # value = {'idle': <Mode.idle: 0>, 'position': <Mode.position: 1>, 'velocity': <Mode.velocity: 2>, 'effort': <Mode.effort: 3>}
    effort: typing.ClassVar[Mode]  # value = <Mode.effort: 3>
    idle: typing.ClassVar[Mode]  # value = <Mode.idle: 0>
    position: typing.ClassVar[Mode]  # value = <Mode.position: 1>
    velocity: typing.ClassVar[Mode]  # value = <Mode.velocity: 2>
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class Model:
    """
    @brief Robot models
    
    Members:
    
      wxai_v0 : @brief WXAI V0
    """
    __members__: typing.ClassVar[dict[str, Model]]  # value = {'wxai_v0': <Model.wxai_v0: 0>}
    wxai_v0: typing.ClassVar[Model]  # value = <Model.wxai_v0: 0>
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class StandardEndEffector:
    """
    @brief End effector properties for the standard variants
    """
    wxai_v0_base: typing.ClassVar[EndEffectorProperties]  # value = <trossen_arm.trossen_arm.EndEffectorProperties object>
    wxai_v0_follower: typing.ClassVar[EndEffectorProperties]  # value = <trossen_arm.trossen_arm.EndEffectorProperties object>
    wxai_v0_leader: typing.ClassVar[EndEffectorProperties]  # value = <trossen_arm.trossen_arm.EndEffectorProperties object>
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self) -> None:
        ...
class TrossenArmDriver:
    """
    @brief Trossen Arm Driver
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self) -> None:
        ...
    def cleanup(self) -> None:
        """
                @brief Cleanup the driver
        """
    def configure(self, model: Model, end_effector: EndEffectorProperties, serv_ip: str, clear_error: bool) -> None:
        """
                @brief Configure the driver
        
                @param model Model of the robot
                @param end_effector End effector properties
                @param serv_ip IP address of the robot
                @param clear_error Whether to clear the error state of the robot
        """
    def get_dns(self) -> str:
        """
                @brief Get the DNS
        
                @return DNS address
        """
    def get_effort_correction(self) -> list[float]:
        """
                @brief Get the effort correction
        
                @return Effort correction
        
                @note This configuration is used to map the efforts in Nm or N to the motor
                  effort unit, i.e., effort_correction = motor effort unit / Nm or N
        """
    def get_efforts(self) -> list[float]:
        """
                @brief Get the efforts
        
                @return Efforts in Nm for arm joints and N for the gripper joint
        """
    def get_end_effector(self) -> EndEffectorProperties:
        """
                @brief Get the end effector mass properties
        
                @return The end effector mass property structure
        """
    def get_error_information(self) -> str:
        """
                @brief Get the error information of the robot
        
                @return Error information
        """
    def get_external_efforts(self) -> list[float]:
        """
                @brief Get the external efforts
        
                @return External efforts in Nm for arm joints and N for the gripper joint
        """
    def get_factory_reset_flag(self) -> bool:
        """
                @brief Get the factory reset flag
        
                @return true if the configurations will be reset to factory defaults at the next startup
                @return false if the configurations will not be reset to factory defaults at the next startup
        """
    def get_gateway(self) -> str:
        """
                @brief Get the gateway
        
                @return Gateway address
        """
    def get_ip_method(self) -> IPMethod:
        """
                @brief Get the IP method
        
                @return IP method
        """
    def get_manual_ip(self) -> str:
        """
                @brief Get the manual IP
        
                @return Manual IP address
        """
    def get_modes(self) -> list[Mode]:
        """
                @brief Get the modes
        
                @return Modes of all joints, a list of Modes
        """
    def get_num_joints(self) -> int:
        """
                @brief Get the number of joints
        
                @return Number of joints
        """
    def get_positions(self) -> list[float]:
        """
                @brief Get the positions
        
                @return Positions in rad for arm joints and m for the gripper joint
        """
    def get_subnet(self) -> str:
        """
                @brief Get the subnet
        
                @return Subnet address
        """
    def get_velocities(self) -> list[float]:
        """
                @brief Get the velocities
        
                @return Velocities in rad/s for arm joints and m/s for the gripper joint
        """
    def set_all_efforts(self, goal_efforts: list[float], goal_time: float = 2.0, blocking: bool = True) -> None:
        """
                @brief Set the efforts of all joints
        
                @param goal_efforts Efforts in Nm for arm joints and N for the gripper joint
                @param goal_time Optional: goal time in s when the goal efforts should be reached, default
                  2.0s
                @param blocking Optional: whether to block until the goal efforts are reached, default true
        
                @note The size of the vectors should be equal to the number of joints
        """
    def set_all_modes(self, mode: Mode = ...) -> None:
        """
                @brief Set all joints to the same mode
        
                @param mode Mode for all joints, one of
                  Mode.idle
                  Mode.position
                  Mode.velocity
                  Mode.effort
        """
    def set_all_positions(self, goal_positions: list[float], goal_time: float = 2.0, blocking: bool = True, goal_feedforward_velocities: list[float] | None = None, goal_feedforward_accelerations: list[float] | None = None) -> None:
        """
                @brief Set the positions of all joints
        
                @param goal_positions Positions in rad for arm joints and m for the gripper joint
                @param goal_time Optional: goal time in s when the goal positions should be reached, default
                  2.0s
                @param blocking Optional: whether to block until the goal positions are reached, default
                  true
                @param goal_feedforward_velocities Optional: feedforward velocities in rad/s for arm joints
                  and m/s for the gripper joint, default zeros
                @param goal_feedforward_accelerations Optional: feedforward accelerations in rad/s^2 for arm
                  joints and m/s^2 for the gripper joint, default zeros
        
                @note The size of the vectors should be equal to the number of joints
        """
    def set_all_velocities(self, goal_velocities: list[float], goal_time: float = 2.0, blocking: bool = True, goal_feedforward_accelerations: list[float] | None = None) -> None:
        """
                @brief Set the velocities of all joints
        
                @param goal_velocities Velocities in rad/s for arm joints and m/s for the gripper joint
                @param goal_time Optional: goal time in s when the goal velocities should be reached,
                  default 2.0s
                @param blocking Optional: whether to block until the goal velocities are reached, default
                  true
                @param goal_feedforward_accelerations Optional: feedforward accelerations in rad/s^2 for arm
                  joints and m/s^2 for the gripper joint, default zeros
        
                @note The size of the vectors should be equal to the number of joints
        """
    def set_arm_efforts(self, goal_efforts: list[float], goal_time: float = 2.0, blocking: bool = True) -> None:
        """
                @brief Set the efforts of the arm joints
        
                @param goal_efforts Efforts in Nm
                @param goal_time Optional: goal time in s when the goal efforts should be reached, default
                  2.0s
                @param blocking Optional: whether to block until the goal efforts are reached, default true
        
                @note The size of the vectors should be equal to the number of arm joints
        """
    def set_arm_modes(self, mode: Mode = ...) -> None:
        """
                @brief Set the mode of the arm joints
        
                @param mode Mode for the arm joints, one of
                  Mode.idle
                  Mode.position
                  Mode.velocity
                  Mode.effort
        
                @warning This method does not change the gripper joint's mode
        """
    def set_arm_positions(self, goal_positions: list[float], goal_time: float = 2.0, blocking: bool = True, goal_feedforward_velocities: list[float] | None = None, goal_feedforward_accelerations: list[float] | None = None) -> None:
        """
                @brief Set the positions of the arm joints
        
                @param goal_positions Positions in rad
                @param goal_time Optional: goal time in s when the goal positions should be reached, default
                  2.0s
                @param blocking Optional: whether to block until the goal positions are reached, default
                  true
                @param goal_feedforward_velocities Optional: feedforward velocities in rad/s, default zeros
                @param goal_feedforward_accelerations Optional: feedforward accelerations in rad/s^2,
                  default zeros
        
                @note The size of the vectors should be equal to the number of arm joints
        """
    def set_arm_velocities(self, goal_velocities: list[float], goal_time: float = 2.0, blocking: bool = True, goal_feedforward_accelerations: list[float] | None = None) -> None:
        """
                @brief Set the velocities of the arm joints
        
                @param goal_velocities Velocities in rad
                @param blocking Optional: whether to block until the goal velocities are reached, default
                  true
                @param goal_time Optional: goal time in s when the goal velocities should be reached,
                  default 2.0s
                @param goal_feedforward_accelerations Optional: feedforward accelerations in rad/s^2,
                  default zeros
        
                @note The size of the vectors should be equal to the number of arm joints
        """
    def set_dns(self, dns: str = '8.8.8.8') -> None:
        """
                @brief Set the DNS
        
                @param dns DNS address
        """
    def set_effort_correction(self, effort_correction: list[float]) -> None:
        """
                @brief Set the effort correction
        
                @param effort_correction The effort correction to set
        
                @note This configuration is used to map the efforts in Nm or N to the motor
                  effort unit, i.e., effort_correction = motor effort unit / Nm or N
        """
    def set_end_effector(self, end_effector: EndEffectorProperties) -> None:
        """
                @brief Set the end effector properties
        
                @param end_effector The end effector properties
        """
    def set_factory_reset_flag(self, flag: bool = True) -> None:
        """
                @brief Set the factory reset flag
        
                @param flag Whether to reset the configurations to factory defaults at the next startup
        """
    def set_gateway(self, gateway: str = '192.168.1.1') -> None:
        """
                @brief Set the gateway
        
                @param gateway Gateway address
        """
    def set_gripper_effort(self, goal_effort: float, goal_time: float = 2.0, blocking: bool = True) -> None:
        """
                @brief Set the effort of the gripper
        
                @param goal_effort Effort in N
                @param goal_time Optional: goal time in s when the goal effort should be reached, default
                  2.0s
                @param blocking Optional: whether to block until the goal effort is reached, default true
        """
    def set_gripper_mode(self, mode: Mode = ...) -> None:
        """
                @brief Set the mode of the gripper joint
        
                @param mode Mode for the gripper joint, one of
                  Mode.idle
                  Mode.position
                  Mode.velocity
                  Mode.effort
        
                @warning This method does not change the arm joints' mode
        """
    def set_gripper_position(self, goal_position: float, goal_time: float = 2.0, blocking: bool = True, goal_feedforward_velocity: float = 0.0, goal_feedforward_acceleration: float = 0.0) -> None:
        """
                @brief Set the position of the gripper
        
                @param goal_position Position in m
                @param goal_time Optional: goal time in s when the goal position should be reached, default
                  2.0s
                @param blocking Optional: whether to block until the goal position is reached, default true
                @param goal_feedforward_velocity Optional: feedforward velocity in m/s, default zero
                @param goal_feedforward_acceleration Optional: feedforward acceleration in m/s^2, default
                  zero
        """
    def set_gripper_velocity(self, goal_velocity: float, goal_time: float = 2.0, blocking: bool = True, goal_feedforward_acceleration: float = 0.0) -> None:
        """
                @brief Set the velocity of the gripper
        
                @param goal_velocity Velocity in m/s
                @param goal_time Optional: goal time in s when the goal velocity should be reached, default
                  2.0s
                @param blocking Optional: whether to block until the goal velocity is reached, default true
                @param goal_feedforward_acceleration Optional: feedforward acceleration in m/s^2, default
                  zero
        """
    def set_ip_method(self, method: IPMethod = ...) -> None:
        """
                @brief Set the IP method
        
                @param method The IP method to set, one of IPMethod.manual or IPMethod.dhcp
        """
    def set_joint_effort(self, joint_index: int, goal_effort: float, goal_time: float = 2.0, blocking: bool = True) -> None:
        """
                @brief Set the effort of a joint
        
                @param joint_index The index of the joint in [0, num_joints - 1]
                @param goal_effort Effort in Nm for arm joints and N for the gripper joint
                @param goal_time Optional: goal time in s when the goal effort should be reached, default
                  2.0s
                @param blocking Optional: whether to block until the goal effort is reached, default true
        """
    def set_joint_modes(self, modes: list[Mode]) -> None:
        """
                @brief Set the modes of each joint
        
                @param modes Desired modes for each joint, one of
                  Mode.idle
                  Mode.position
                  Mode.velocity
                  Mode.effort
        """
    def set_joint_position(self, joint_index: int, goal_position: float, goal_time: float = 2.0, blocking: bool = True, goal_feedforward_velocity: float = 0.0, goal_feedforward_acceleration: float = 0.0) -> None:
        """
                @brief Set the position of a joint
        
                @param joint_index The index of the joint in [0, num_joints - 1]
                @param goal_position Position in rad for arm joints and m for the gripper joint
                @param goal_time Optional: goal time in s when the goal position should be reached, default
                  2.0s
                @param blocking Optional: whether to block until the goal position is reached, default true
                @param goal_feedforward_velocity Optional: feedforward velocity in rad/s for arm joints and
                  m/s for the gripper joint, default zero
                @param goal_feedforward_acceleration Optional: feedforward acceleration in rad/s^2 for arm
                  joints and m/s^2 for the gripper joint, default zero
        """
    def set_joint_velocity(self, joint_index: int, goal_velocity: float, goal_time: float = 2.0, blocking: bool = True, goal_feedforward_acceleration: float = 0.0) -> None:
        """
                @brief Set the velocity of a joint
        
                @param joint_index The index of the joint in [0, num_joints - 1]
                @param goal_velocity Velocity in rad/s for arm joints and m/s for the gripper joint
                @param goal_time Optional: goal time in s when the goal velocity should be reached, default
                  2.0s
                @param blocking Optional: whether to block until the goal velocity is reached, default true
                @param goal_feedforward_acceleration Optional: feedforward acceleration in rad/s^2 for arm
                  joints and m/s^2 for the gripper joint, default zero
        """
    def set_manual_ip(self, manual_ip: str = '192.168.1.2') -> None:
        """
                @brief Set the manual IP
        
                @param manual_ip Manual IP address
        """
    def set_subnet(self, subnet: str = '255.255.255.0') -> None:
        """
                @brief Set the subnet
        
                @param subnet Subnet address
        """
