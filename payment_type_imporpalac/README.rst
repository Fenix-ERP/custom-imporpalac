=======================
Payment type Imporpalac
=======================

.. !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   !! This file is generated by oca-gen-addon-readme !!
   !! changes will be overwritten.                   !!
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

.. |badge1| image:: https://img.shields.io/badge/maturity-Beta-yellow.png
    :target: https://odoo-community.org/page/development-status
    :alt: Beta
.. |badge2| image:: https://img.shields.io/badge/licence-AGPL--3-blue.png
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3
.. |badge3| image:: https://img.shields.io/badge/github-OCA%2Fcustom--imporpalac-lightgray.png?logo=github
    :target: https://github.com/OCA/custom-imporpalac/tree/14.0/payment_type_imporpalac
    :alt: OCA/custom-imporpalac
.. |badge4| image:: https://img.shields.io/badge/weblate-Translate%20me-F47D42.png
    :target: https://translation.odoo-community.org/projects/custom-imporpalac-14-0/custom-imporpalac-14-0-payment_type_imporpalac
    :alt: Translate me on Weblate

|badge1| |badge2| |badge3| |badge4| 

This module extends the sales functionality, allows you to add a percentage to the quote when charging for payment by credit card

**Table of contents**

.. contents::
   :local:

Installation
============

To install this module, you need to:

#. Copy module files to addon folder.
#. Restart odoo service (sudo service odoo-server restart).
#. Go to your odoo instance and open apps (make sure to activate debug mode).
#. click on update app list.
#. search module name and hit install button.

Configuration
=============

In settings write the additional percentage to be charged for payment by credit card in the field: Tax credit card

Usage
=====

To use this module, you need to:

#. Make sure to add the extra percentage to charge in settings
#. Go to the Sales module.
#. Create new quotation.
#. Select the type of payment or create new.

Known issues / Roadmap
======================

* Code optimization.

Changelog
=========

14.0.1.0.0 (2022-10-21)
* [ADD] : Module for payment type imporpalac

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/custom-imporpalac/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and welcomed
`feedback <https://github.com/OCA/custom-imporpalac/issues/new?body=module:%20payment_type_imporpalac%0Aversion:%2014.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Do not contact contributors directly about support or help with technical issues.

Credits
=======

Authors
~~~~~~~

* Bryan Sandoval

Contributors
~~~~~~~~~~~~

Bryan Sandoval <bryansandoval300@gmail.com>

Maintainers
~~~~~~~~~~~

This module is maintained by the OCA.

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

This module is part of the `OCA/custom-imporpalac <https://github.com/OCA/custom-imporpalac/tree/14.0/payment_type_imporpalac>`_ project on GitHub.

You are welcome to contribute. To learn how please visit https://odoo-community.org/page/Contribute.
