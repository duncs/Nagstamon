# encoding: utf-8

import os
import platform
import sys
import ConfigParser
import base64
import zlib
import sys

class Config(object):
    """
        The place for central configuration.
    """
    def __init__(self):
        """
            read config file and set the appropriate attributes
        """
        # supposed to be sensible defaults
        self.update_interval = 1
        self.short_display = False
        self.long_display = True
        self.show_grid = True
        self.filter_all_down_hosts = False
        self.filter_all_unreachable_hosts = False
        self.filter_all_flapping_hosts = False
        self.filter_all_unknown_services = False
        self.filter_all_warning_services = False
        self.filter_all_critical_services = False
        self.filter_all_flapping_services = False
        self.filter_acknowledged_hosts_services = False
        self.filter_hosts_services_disabled_notifications = False
        self.filter_hosts_services_disabled_checks = False
        self.filter_hosts_services_maintenance = False
        self.filter_services_on_acknowledged_hosts = False        
        self.filter_services_on_down_hosts = False
        self.filter_services_on_hosts_in_maintenance = False
        self.filter_services_on_unreachable_hosts = False
        self.filter_services_in_soft_state = False
        self.position_x = 30
        self.position_y = 30
        self.popup_details_hover = True
        self.popup_details_clicking = False
        self.close_details_hover = True
        self.close_details_clicking = False
        self.connect_by_host = True
        self.connect_by_dns = False
        self.connect_by_ip = False
        self.debug_mode = False
        self.debug_to_file = False
        self.debug_file = os.path.expanduser('~') + os.sep + "nagstamon.log"
        self.check_for_new_version = True
        self.notification = True
        self.notification_flashing = True
        # because of nonexistent windows systray popup support I'll let it be now
        #self.notification_popup = False
        self.notification_sound = True
        self.notification_sound_repeat = False
        self.notification_default_sound = True
        self.notification_custom_sound = False      
        self.notification_custom_sound_warning = None
        self.notification_custom_sound_critical = None
        self.notification_custom_sound_down = None
        self.notify_if_warning = True
        self.notify_if_critical = True
        self.notify_if_unknown = True
        self.notify_if_unreachable = True
        self.notify_if_down = True
        self.re_host_enabled = False
        self.re_host_pattern = ""
        self.re_host_reverse = False
        self.re_service_enabled = False
        self.re_service_pattern = ""
        self.re_service_reverse = False
        self.re_status_information_enabled = False
        self.re_status_information_pattern = ""
        self.re_status_information_reverse = False
        self.color_ok_text = self.default_color_ok_text = "#FFFFFF"
        self.color_ok_background = self.default_color_ok_background = "#006400"
        self.color_warning_text = self.default_color_warning_text = "#000000"
        self.color_warning_background = self.default_color_warning_background = "#FFFF00"
        self.color_critical_text = self.default_color_critical_text = "#FFFFFF"
        self.color_critical_background = self.default_color_critical_background = "#FF0000"
        self.color_unknown_text = self.default_color_unknown_text = "#000000"
        self.color_unknown_background = self.default_color_unknown_background = "#FFA500"
        self.color_unreachable_text = self.default_color_unreachable_text = "#FFFFFF"
        self.color_unreachable_background = self.default_color_unreachable_background = "#8B0000"        
        self.color_down_text = self.default_color_down_text = "#FFFFFF"
        self.color_down_background = self.default_color_down_background = "#000000"
        self.color_error_text = self.default_color_error_text= "#000000"
        self.color_error_background = self.default_color_error_background = "#D3D3D3"
        self.statusbar_systray = False
        self.statusbar_floating = True
        self.icon_in_systray = False  
        self.systray_popup_offset= 10
        self.defaults_acknowledge_sticky = False
        self.defaults_acknowledge_send_notification = False
        self.defaults_acknowledge_persistent_comment = False
        self.defaults_acknowledge_all_services = False
        self.defaults_acknowledge_comment = "acknowledged"
        self.defaults_submit_check_result_comment = "check result submitted"
        self.defaults_downtime_duration_hours = 2
        self.defaults_downtime_duration_minutes = 0
        self.defaults_downtime_comment = "scheduled downtime"
        self.defaults_downtime_type_fixed = True
        self.defaults_downtime_type_flexible = False

        """
        # those are example Windows settings, almost certainly a
        # user will have to fix them for his computer
        if platform.system() == "Windows":
            self.app_ssh_bin = "C:\Program Files\PuTTY\putty.exe"
            self.app_rdp_bin = "C:\windows\system32\mstsc.exe"
            self.app_vnc_bin = "C:\Program Files\TightVNC\\vncviewer.exe"
            self.app_ssh_options = "-l root"
            self.app_rdp_options = "/v:"
            self.app_vnc_options = ""
        else:
            # the Linux settings
            self.app_ssh_bin = "/usr/bin/gnome-terminal -x ssh"
            self.app_rdp_bin = "/usr/bin/rdesktop"
            self.app_vnc_bin = "/usr/bin/vncviewer"
            self.app_ssh_options = "-l root"
            self.app_rdp_options = "-g 1024x768"
            self.app_vnc_options = ""
        """
        
        # the app is unconfigured by default and will stay so if it
        # would not find a config file
        self.unconfigured = True
        
        # try to use a given config file - there must be one given
        # if sys.argv is larger than 1
        if len(sys.argv) > 1:
            if sys.argv[1].find("-psn") != -1:
                # new configdir approach
                self.configdir = os.path.expanduser('~') + os.sep + ".nagstamon"
            else:
                # allow to give a config file
                self.configdir = sys.argv[1]
                           
        # otherwise if there exits a configfile in current working directory it should be used
        elif os.path.exists(os.getcwd() + os.sep + "nagstamon.config"):
            self.configdir = os.getcwd() + os.sep + "nagstamon.config"
        else:
            # ~/.nagstamon/nagstamon.conf is the user conf file
            # os.path.expanduser('~') finds out the user HOME dir where 
            # nagstamon expects its conf file to be
            self.configdir = os.path.expanduser('~') + os.sep + ".nagstamon"

        self.configfile = self.configdir + os.sep + "nagstamon.conf"            
            
        # make path fit for actual os, normcase for letters and normpath for path
        self.configfile = os.path.normpath(os.path.normcase(self.configfile))

        # because the name of the configdir is also stored in the configfile
        # there may be situations where the name gets overwritten by a
        # wrong name so it will be stored here temporarily
        configdir_temp = self.configdir
        
        # default settings dicts
        self.servers = dict()
        self.actions = dict()
        
        if os.path.exists(self.configfile):
            # instantiate a Configparser to parse the conf file
            # SF.net bug #3304423 could be fixed with allow_no_value argument which
            # is only available since Python 2.7
            if sys.version_info[0] < 3 and sys.version_info[1] < 7:
                config = ConfigParser.ConfigParser()
            else:
                config = ConfigParser.ConfigParser(allow_no_value=True)
            config.read(self.configfile)
            
            # go through all sections of the conf file
            for section in config.sections():
                # go through all items of each sections (in fact there is only on
                # section which has to be there to comply to the .INI file standard
                for i in config.items(section):
                    # create a key of every config item with its appropriate value
                    object.__setattr__(self, i[0], i[1])
                    
            # reset self.configdir to temporarily saved value in case it differs from
            # the one read from configfile and so it would fail to save next time
            self.configdir = configdir_temp
                        
            # seems like there is a config file so the app is not unconfigured anymore
            self.unconfigured = False

            # Servers configuration...
            self.servers = self._LoadServersMultipleConfig()
         
            # Load actions
            self.actions = self.LoadMultipleConfig("actions", "action", "Action")

            
    def _LoadServersMultipleConfig(self):
        """
        load servers config - special treatment because of obfuscated passwords
        """
        servers = self.LoadMultipleConfig("servers", "server", "Server")
        # deobfuscate username + password inside a try-except loop
        # if entries have not been obfuscated yet this action should raise an error
        # and old values (from nagstamon < 0.9.0) stay and will be converted when next
        # time saving config        
        try:
            for server in servers:
                servers[server].username = self.DeObfuscate(servers[server].username)
                if servers[server].save_password == "False":
                    servers[server].password = ""
                else:
                    servers[server].password = self.DeObfuscate(servers[server].password)
                servers[server].proxy_username = self.DeObfuscate(servers[server].proxy_username)
                servers[server].proxy_password = self.DeObfuscate(servers[server].proxy_password)
        except:
            import traceback
            traceback.print_exc(file=sys.stdout)   
        
        return servers
            
                        
    def LoadMultipleConfig(self, settingsdir, setting, configobj):
        """
        load generic config into settings dict and return to central config
        """
        # defaults as empty dict in case settings dir/files could not be found
        settings = dict()
        
        try:
            if os.path.exists(self.configdir + os.sep + settingsdir):
                # dictionary that later gets returned back
                settings = dict()
                for f in os.listdir(self.configdir + os.sep + settingsdir):
                    if f.startswith(setting + "_") and f.endswith(".conf"):
                        if sys.version_info[0] < 3 and sys.version_info[1] < 7:
                            config = ConfigParser.ConfigParser()
                        else:
                            config = ConfigParser.ConfigParser(allow_no_value=True)
                        config.read(self.configdir + os.sep + settingsdir + os.sep + f)
                        
                        # create object for every setting
                        name = f.split("_", 1)[1].rpartition(".")[0]
                        settings[name] = globals()[configobj]()                 

                        # go through all items of the server
                        for i in config.items(setting + "_" + name):
                            # create a key of every config item with its appropriate value
                            settings[name].__setattr__(i[0], i[1])
        except:
            import traceback
            traceback.print_exc(file=sys.stdout)
        
        return settings
            

    def SaveConfig(self, output):
        """
            save config file
        """
        try:
            # Make sure .nagstamon is created
            if not os.path.exists(self.configdir):
                os.mkdir(self.configdir)
            # save config file with ConfigParser
            config = ConfigParser.ConfigParser()
            # general section for Nagstamon
            config.add_section("Nagstamon")
            for option in self.__dict__:
                if not option in ["servers", "actions"]:
                    config.set("Nagstamon", option, self.__dict__[option])

            # save servers dict
            self.SaveMultipleConfig("servers", "server")

            # save actions dict
            self.SaveMultipleConfig("actions", "action")

            # debug
            if str(self.debug_mode) == "True":
                output.servers.values()[0].Debug(server="", debug="Saving config to" + self.configfile)
                
            # open, save and close config file
            f = open(os.path.normpath(self.configfile), "w")
            config.write(f)
            f.close()           
        except:
            # debug
            if str(self.debug_mode) == "True":
                output.servers.values()[0].Error(sys.exc_info())
            
            
    def SaveMultipleConfig(self, settingsdir, setting):
        """
        saves conf files for settings like actions in extra directories
        "multiple" means that multiple confs for actions or servers are loaded,
        not just one like for e.g. sound file
        """
        try:
            # one section for each setting
            for s in self.__dict__[settingsdir]:
                # depending on python version allow_no_value is allowed or not
                if sys.version_info[0] < 3 and sys.version_info[1] < 7:
                    config = ConfigParser.ConfigParser()
                else:
                    config = ConfigParser.ConfigParser(allow_no_value=True)
                config.add_section(setting + "_" + s)
                for option in self.__dict__[settingsdir][s].__dict__:
                    # obfuscate certain entries in config file - special arrangement for servers
                    if settingsdir == "servers":
                        if option == "username" or option == "password" or option == "proxy_username" or option == "proxy_password":
                            value = self.Obfuscate(self.__dict__[settingsdir][s].__dict__[option])
                            if option == "password" \
                               and self.__dict__[settingsdir][s].save_password == "False":
                                value = ""
                            config.set(setting + "_" + s, option, value)
                        else:
                            config.set(setting + "_" + s, option, self.__dict__[settingsdir][s].__dict__[option])
                    else:
                        config.set(setting + "_" + s, option, self.__dict__[settingsdir][s].__dict__[option])
                        
                # open, save and close config_server file
                if not os.path.exists(self.configdir + os.sep + settingsdir):
                    os.mkdir(self.configdir + os.sep + settingsdir)
                f = open(os.path.normpath(self.configdir + os.sep + settingsdir + os.sep + setting + "_" + s + ".conf"), "w")
                config.write(f)
                f.close()
                
            # clean up old deleted/renamed config files
            for f in os.listdir(self.configdir + os.sep + settingsdir):
                if not f.split(setting + "_")[1].split(".conf")[0] in self.__dict__[settingsdir]:
                    os.unlink(self.configdir + os.sep + settingsdir + os.sep + f)
            
        except:
            import traceback
            traceback.print_exc(file=sys.stdout)
            
            
    def Convert_Conf_to_Multiple_Servers(self):
        """
            if there are settings found which come from older nagstamon version convert them -
            now with multiple servers support these servers have their own settings
        
            DEPRECATED I think, after 2,5 years have passed there should be no version less than 0.8.0 in the wild...
        """
        
        # check if old settings exist
        if self.__dict__.has_key("nagios_url") and \
            self.__dict__.has_key("nagios_cgi_url") and \
            self.__dict__.has_key("username") and \
            self.__dict__.has_key("password") and \
            self.__dict__.has_key("use_proxy_yes") and \
            self.__dict__.has_key("use_proxy_no"):
            # create Server and fill it with old settings
            server_name = "Default"
            self.servers[server_name] = Server()
            self.servers[server_name].name = server_name
            self.servers[server_name].nagios_url = self.nagios_url
            self.servers[server_name].nagios_cgi_url = self.nagios_cgi_url
            self.servers[server_name].username = self.username
            self.servers[server_name].password = self.password
            # convert VERY old config files
            try:
                self.servers[server_name].use_proxy = self.use_proxy_yes
            except:
                self.servers[server_name].use_proxy = False
            try:
                self.servers[server_name].use_proxy_from_os = self.use_proxy_from_os_yes
            except:
                self.servers[server_name].use_proxy_from_os = False
            # delete old settings from config
            self.__dict__.pop("nagios_url")
            self.__dict__.pop("nagios_cgi_url")
            self.__dict__.pop("username")
            self.__dict__.pop("password")
            self.__dict__.pop("use_proxy_yes")
            self.__dict__.pop("use_proxy_no")
            
            # save config
            #self.SaveConfig()
            
            
    def Convert_Conf_to_Custom_Actions(self):
        """
        any nagstamon minor to 0.9.9 will have extra ssh/rdp/vnc settings
        which will be converted to custom actions here
        """
        
        # check if old settings exist
        if self.__dict__.has_key("app_ssh_bin") and \
            self.__dict__.has_key("app_ssh_options") and \
            self.__dict__.has_key("app_rdp_bin") and \
            self.__dict__.has_key("app_rdp_options") and \
            self.__dict__.has_key("app_vnc_bin") and \
            self.__dict__.has_key("app_vnc_options"):
            # create actions and fill them with old settings
            self.actions["SSH"] = Action()
            self.actions["SSH"].type = "command"
            self.actions["SSH"].name = "SSH"
            self.actions["SSH"].string = self.app_ssh_bin + " " + self.app_ssh_options + " $ADDRESS$"
            self.actions["SSH"].description = "Converted from pre 0.9.9 Nagstamon."
            self.actions["RDP"] = Action()
            self.actions["RDP"].type = "command"
            self.actions["RDP"].name = "RDP"
            self.actions["RDP"].string = self.app_rdp_bin + " " + self.app_rdp_options + " $ADDRESS$"
            self.actions["RDP"].description = "Converted from pre 0.9.9 Nagstamon."
            self.actions["VNC"] = Action()
            self.actions["VNC"].type = "command"
            self.actions["VNC"].name = "VNC"
            self.actions["VNC"].string = self.app_vnc_bin + " " + self.app_vnc_options + " $ADDRESS$"
            self.actions["VNC"].description = "Converted from pre 0.9.9 Nagstamon."
            
            # delete old settings from config
            self.__dict__.pop("app_ssh_bin")
            self.__dict__.pop("app_ssh_options")
            self.__dict__.pop("app_rdp_bin")
            self.__dict__.pop("app_rdp_options")
            self.__dict__.pop("app_vnc_bin")
            self.__dict__.pop("app_vnc_options")
            
        
    def Obfuscate(self, string, count=5):
        """
            Obfuscate a given string to store passwords etc.
        """
        for i in range(count):
            string = list(base64.b64encode(string))
            string.reverse()
            string = "".join(string)
            string = zlib.compress(string)
        string = base64.b64encode(string)
        return string


    def DeObfuscate(self, string, count=5):
        string = base64.b64decode(string)
        for i in range(count):
            string = zlib.decompress(string)
            string = list(string)
            string.reverse()   
            string = "".join(string)    
            string = base64.b64decode(string)
        return string
    

class Server(object):
    """
    one Server realized as object for config info
    """
    def __init__(self):
        self.enabled = True
        self.type = "Nagios"
        self.name = ""
        self.nagios_url = ""
        self.nagios_cgi_url = ""
        self.username = ""
        self.password = ""
        self.save_password = True
        self.use_proxy = False
        self.use_proxy_from_os = False
        self.proxy_address = ""
        self.proxy_username = ""
        self.proxy_password = ""
        

class Action(object):
    """
    class for custom actions, which whill be thrown into one config dictionary like the servers
    """
    
    def __init__(self):
        # to be or not to be enabled...
        self.enabled = True
        # one of those: browser, url or command
        self.type = "browser"
        # thy name is...
        self.name = "Custom action"
        # OS of host where Nagstamon runs - especially commands are mostly not platform agnostic
        self.os = ""
        # description
        self.description = "Starts a custom action."
        # might be URL in case of type browser/url and a commandline for commands
        self.string = ""
        # who did this
        self.author = "Nag Stamon"
        # version - maybe in future this might be more sophisticated
        self.version = "1"
        # kind of Nagios item this action is targeted to - maybe also usable for states
        self.filter_target_host = True
        self.filter_target_service = True
        # action applies only to certain hosts or services
        self.filter_host = ""
        self.filter_host_reverse = False
        self.filter_service = ""
        self.filter_service_reverse = False
    