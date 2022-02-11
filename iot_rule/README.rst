.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

========
IoT Rule
========

This module define Rules, i.e. defines the Inputs that can be controlled by a certain Key.

An Agent (which can be an Employee, a Partner or a Visitor) is the owner of one and only one Key.

The Input is a request from an IoT Device that executes a certain function in Odoo.

This function will check if the Key (= the Agent) is allowed by any Rule to "control" the Device.

If Odoo answers positively the Agent will be allowed the IoT Device to execute some Function: for example open a door or switch on a relay.
