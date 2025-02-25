phpmyadmin plugin for `Tutor <https://docs.tutor.edly.io>`__
############################################################

This is a `Tutor`_ plugin that provides an easy way to manage your MySQL databases through a web interface using phpMyAdmin.

.. image:: https://raw.githubusercontent.com/CodeWithEmad/tutor-contrib-phpmyadmin/master/docs/screenshot.png
    :alt: PHPMyAdmin in action

Installation
************

Ensure you are using Tutor v15+ (Olive onwards). First, install the plugin by running:

.. code-block:: bash

    pip install -U tutor-contrib-phpmyadmin
    # or
    pip install git+https://github.com/CodeWithEmad/tutor-contrib-phpmyadmin

Enable the plugin and run the launch command:

.. code-block:: bash

    tutor plugins enable phpmyadmin
    tutor dev|local|k8s launch

Alternatively, if you already have a running Open edX instance, just start the phpmyadmin service:

.. code-block:: bash

    tutor dev|local|k8s start phpmyadmin

Access phpMyAdmin at: http://phpmyadmin.local.edly.io:8081 (local) or https://phpmyadmin.yourdomain.com (production)

**Important**

Enabling phpMyAdmin can be useful for managing your WordPress database directly. However, please be aware that exposing
phpMyAdmin can pose security risks if not properly secured. Ensure that you have strong passwords, and consider
restricting access to phpMyAdmin to trusted IP addresses only.


Variables
*********

The following variables can be configured to customize the phpMyAdmin plugin:

- ``PHPMYADMIN_HOST``: phpMyAdmin hostname (default: phpmyadmin.local.edly.io)
- ``PHPMYADMIN_PORT``: phpMyAdmin port (default: 8081)
- ``PHPMYADMIN_DOCKER_IMAGE``: Docker image for phpMyAdmin (default: phpmyadmin:5.2.1)
- ``PHPMYADMIN_UPLOAD_LIMIT``: phpMyAdmin upload limit (default: 50M)

Contributing
************

We welcome all contributions! Feel free to open a Pull Request or an Issue.

License
*******

This software is licensed under the terms of the `AGPLv3`_.

.. _Tutor: https://docs.tutor.edly.io
.. _AGPLv3: https://github.com/codewithemad/tutor-contrib-phpmyadmin/blob/master/LICENSE.txt
