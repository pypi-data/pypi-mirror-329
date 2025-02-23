=============
SELF DESTRUCT
=============

.. image:: https://img.shields.io/pypi/v/self-destruct.svg?style=for-the-badge
   :target: https://pypi.org/project/self-destruct/

``self-destruct`` is a simple Python library for stopping and terminating EC2
instances from within themselves, which is not officially supported by AWS.
Usage is very simple:

.. code-block:: python

    from self_destruct import self_destruct

    self_destruct()

The only customization option is the specification of a parameter
``terminate: bool = True`` which allows the user to specify whether they want to
terminate the instance or merely stop it.

Note that in order for this function to be successful, the EC2 instance must
have the following permissions:

::

    "ec2:DescribeInstances"
    "ec2:StopInstances"
    "ec2:TerminateInstances"
