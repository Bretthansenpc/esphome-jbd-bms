import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import switch
from esphome.const import CONF_ICON, CONF_ID

from .. import CONF_JBD_BMS_ID, JbdBms, jbd_bms_ns

DEPENDENCIES = ["jbd_bms"]

CODEOWNERS = ["@syssi"]

CONF_CHARGING = "charging"
CONF_DISCHARGING = "discharging"
CONF_BALANCER = "balancer"
CONF_CHARGE_BALANCER = "charge_balancer"

ICON_DISCHARGING = "mdi:battery-charging-50"
ICON_CHARGING = "mdi:battery-charging-50"
ICON_BALANCER = "mdi:seesaw"
ICON_CHARGE_BALANCER = "mdi:seesaw"

SWITCHES = {
    CONF_DISCHARGING: 0xE1,
    CONF_CHARGING: 0xE1,
    CONF_BALANCER: 0x2D,  # Func mask
    CONF_CHARGE_BALANCER: 0x2D,  # Func mask
}

JbdSwitch = jbd_bms_ns.class_("JbdSwitch", switch.Switch, cg.Component)

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(CONF_JBD_BMS_ID): cv.use_id(JbdBms),
        cv.Optional(CONF_DISCHARGING): switch.SWITCH_SCHEMA.extend(
            {
                cv.GenerateID(): cv.declare_id(JbdSwitch),
                cv.Optional(CONF_ICON, default=ICON_DISCHARGING): switch.icon,
            }
        ).extend(cv.COMPONENT_SCHEMA),
        cv.Optional(CONF_CHARGING): switch.SWITCH_SCHEMA.extend(
            {
                cv.GenerateID(): cv.declare_id(JbdSwitch),
                cv.Optional(CONF_ICON, default=ICON_CHARGING): switch.icon,
            }
        ).extend(cv.COMPONENT_SCHEMA),
        cv.Optional(CONF_BALANCER): switch.SWITCH_SCHEMA.extend(
            {
                cv.GenerateID(): cv.declare_id(JbdSwitch),
                cv.Optional(CONF_ICON, default=ICON_BALANCER): switch.icon,
            }
        ).extend(cv.COMPONENT_SCHEMA),
        cv.Optional(CONF_CHARGE_BALANCER): switch.SWITCH_SCHEMA.extend(
            {
                cv.GenerateID(): cv.declare_id(JbdSwitch),
                cv.Optional(CONF_ICON, default=ICON_CHARGE_BALANCER): switch.icon,
            }
        ).extend(cv.COMPONENT_SCHEMA),
    }
)


def to_code(config):
    hub = yield cg.get_variable(config[CONF_JBD_BMS_ID])
    for key, address in SWITCHES.items():
        if key in config:
            conf = config[key]
            var = cg.new_Pvariable(conf[CONF_ID])
            yield cg.register_component(var, conf)
            yield switch.register_switch(var, conf)
            cg.add(getattr(hub, f"set_{key}_switch")(var))
            cg.add(var.set_parent(hub))
            cg.add(var.set_holding_register(address))
