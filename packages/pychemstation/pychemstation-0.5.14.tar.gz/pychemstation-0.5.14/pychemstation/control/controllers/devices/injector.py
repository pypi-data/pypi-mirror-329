from ....control.controllers import CommunicationController
from .device import DeviceController
from ....utils.injector_types import *
from ....utils.table_types import Table, RegisterFlag


class InjectorController(DeviceController):

    def __init__(self, controller: CommunicationController, table: Table):
        super().__init__(controller, table)

    def get_row(self, row: int) -> InjectorFunction:
        def return_tray_loc() -> Tray:
            pass

        function = self.get_text(row, RegisterFlag.FUNCTION)
        if function == "Wait":
            return Wait(duration=self.get_num(row, RegisterFlag.TIME))
        elif function == "Inject":
            return Inject()
        elif function == "Draw":
            is_source = SourceType(self.get_text(row, RegisterFlag.DRAW_SOURCE))
            is_volume = Mode(self.get_text(row, RegisterFlag.DRAW_VOLUME))
            return Draw(amount=self.get_num(row, RegisterFlag.DRAW_VOLUME_VALUE) if is_volume == Mode.SET else None,
                        source=return_tray_loc() if is_source == SourceType.SPECIFIC_LOCATION else None)
        elif function == "Remote":
            return Remote(command=RemoteCommand(self.get_text(row, RegisterFlag.REMOTE)),
                          duration=self.get_num(row, RegisterFlag.REMOTE_DUR))

    def load(self) -> InjectorTable:
        rows = self.get_num_rows()
        if rows.is_ok():
            return InjectorTable(functions=[self.get_row(i + 1) for i in range(rows.ok_value.num_response)])

    def edit(self, injector_table: InjectorTable):
        self.delete_table()
        res = self.get_num_rows()
        while not res.is_err():
            self.delete_table()
            res = self.get_num_rows()

        self.new_table()
        self.get_num_rows()

        columns_added = set()

        def add_table_val(col_name: RegisterFlag, val: Union[str, int, float]):
            nonlocal columns_added
            if col_name in columns_added:
                if isinstance(val, str):
                    self.edit_row_text(col_name=col_name, val=val)
                else:
                    self.edit_row_num(col_name=col_name, val=val)
            else:
                if isinstance(val, str):
                    self.add_new_col_text(col_name=col_name, val=val)
                else:
                    self.add_new_col_num(col_name=col_name, val=val)
                columns_added.add(col_name)

        def add_inject(inject: Inject):
            add_table_val(col_name=RegisterFlag.FUNCTION, val=inject.__class__.__name__)

        def add_draw(draw: Draw):
            add_table_val(col_name=RegisterFlag.FUNCTION, val=draw.__class__.__name__)
            add_table_val(col_name=RegisterFlag.DRAW_SPEED, val=SourceType.DEFAULT.value)
            add_table_val(col_name=RegisterFlag.DRAW_OFFSET, val=SourceType.DEFAULT.value)

            if draw.amount:
                add_table_val(col_name=RegisterFlag.DRAW_VOLUME, val=Mode.SET.value)
                add_table_val(col_name=RegisterFlag.DRAW_VOLUME_VALUE, val=draw.amount)
            else:
                add_table_val(col_name=RegisterFlag.DRAW_VOLUME, val=Mode.DEFAULT.value)

            if draw.source:
                add_table_val(col_name=RegisterFlag.DRAW_SOURCE, val=SourceType.SPECIFIC_LOCATION.value)
                add_table_val(col_name=RegisterFlag.DRAW_LOCATION_UNIT, val=1)
                add_table_val(col_name=RegisterFlag.DRAW_LOCATION_TRAY, val=1)
                add_table_val(col_name=RegisterFlag.DRAW_LOCATION_ROW, val=1)
                add_table_val(col_name=RegisterFlag.DRAW_LOCATION_COLUMN, val=1)
            else:
                add_table_val(col_name=RegisterFlag.DRAW_SOURCE, val=SourceType.DEFAULT.value)

        def add_wait(wait: Wait):
            add_table_val(col_name=RegisterFlag.FUNCTION, val=wait.__class__.__name__)
            add_table_val(col_name=RegisterFlag.TIME, val=wait.duration)

        def add_remote(remote: Remote):
            add_table_val(col_name=RegisterFlag.FUNCTION, val=remote.__class__.__name__)
            add_table_val(col_name=RegisterFlag.REMOTE, val=remote.command.value)
            add_table_val(col_name=RegisterFlag.REMOTE_DUR, val=remote.duration)

        for i, function in enumerate(injector_table.functions):
            self.add_row()
            if isinstance(function, Inject):
                add_inject(function)
            elif isinstance(function, Draw):
                add_draw(function)
            elif isinstance(function, Wait):
                add_wait(function)
            elif isinstance(function, Remote):
                add_remote(function)
            self.download()

    def download(self):
        pass
