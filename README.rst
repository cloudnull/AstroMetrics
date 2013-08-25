AstroMetrics, The Cloud at your CLI
###################################
:date: 2013-08-14 16:22
:tags: cloud, tool, cli, openstack, rackspace, aws, control
:category: \*nix

Access Your Cloud with ONE Tool
===============================

General Overview
----------------

AstroMetrics is a system by which you can Control your cloud environment using a variety of cloud providers. This CLI tool is being built to work in Openstack environments as well as Rackspace Public Clouds and Amazon AWS.


NOTE
----

This is a 0.0.0 Release of the tool and while I can confirm things do work, you should expect broken-ness


Information
-----------

The backend Library that is doing the heavy lifting is `Apache Libcloud`__ which provides functionality for the majority of cloud providers, however I have only tested and built for the three mentioned providers; Amazon, Openstack, Rackspace.

If you like this project and want to help out, please do. I know that I am not capable of making everything work with every provider for every situation, however with some outside interest we can make it happen.

__ http://libcloud.apache.org/


CLI Client for the Cloud::

    optional arguments:
      -h, --help            show this help message and exit
          --log-level       Set the Log Level {warn, info, error, critical, debug}
          --debug-mode      Uses the standard "stdout" and "stderr" streams while in Daemon Mode
      -V  --version         show program's version number and exit

    Infrastructure Actions:
      <COMMANDS>

        node                Interactions with Cloud Nodes
        list                Listing information from the Cloud Provider
        show                Show information from the Cloud Provider on a resource
        volume              Interactions with Cloud Volumes

    Authentication:
      Authentication against the Cloud API

      -u [USERNAME], --cloud-user     [USERNAME]    Defaults to env[CLOUD_USERNAME]
      -t [USERNAME], --cloud-tenant   [USERNAME]    Defaults to env[CLOUD_TENANT]
      -a [APIKEY],   --cloud-apikey   [APIKEY]      Defaults to env[CLOUD_APIKEY]
      -p [PASSWORD], --cloud-password [PASSWORD]    Defaults to env[CLOUD_PASSWORD]
      -r [REGION],   --cloud-region   [REGION]      Defaults to env[CLOUD_REGION]
                     --cloud-provider [PROVIDER]    Defaults to env[CLOUD_PROVIDER]
                     --cloud-authurl  [AUTH_URL]    Defaults to env[CLOUD_AUTHURL]
                     --cloud-version  [VERSION_NUM] Defaults to env[OS_VERSION]

    2013 All Rights Reserved: