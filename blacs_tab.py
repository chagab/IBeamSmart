from blacs.device_base_class import DeviceTab


class IBeamSmartTab(DeviceTab):

    def initialise_GUI(self):
        do_prop = {'ON': {}}
        ao_prop = {'Power': {
            'base_unit': 'mW',
            'min': 0,
            'max': 10,
            'step': 1e-3,
            'decimals': 1
        }}

        # Create the output objects
        self.create_digital_outputs(do_prop)
        self.create_analog_outputs(ao_prop)

        # Create widgets for output objects
        _, ao_widgets, do_widgets = self.auto_create_widgets()

        # and auto place the widgets in the UI
        self.auto_place_widgets(
            ("Laser ON OFF", do_widgets),
            ("Laser output power", ao_widgets)
        )

        # Store the board number to be used
        connection_object = self.settings['connection_table'].find_by_name(
            self.device_name
        )
        self.board_number = int(connection_object.BLACS_connection)

        # And which scheme we're using for buffered output programming and
        # triggering: (default values for backward compat with old connection
        # tables)
        self.programming_scheme = connection_object.properties.get(
            'programming_scheme',
            'pb_start/BRANCH'
        )

        worker_initialisation_kwargs = \
            self.connection_table.find_by_name(self.device_name).properties
        worker_initialisation_kwargs['addr'] = self.BLACS_connection
        self.create_worker(
            'main_worker',
            'user_devices.IBeamSmart.blacs_worker.IBeamSmartWorker',
            worker_initialisation_kwargs,
        )
        self.primary_worker = 'main_worker'
