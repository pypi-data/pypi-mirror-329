import os
import unittest

from pychemstation.control import HPLCController
from pychemstation.utils.injector_types import *
from pychemstation.utils.tray_types import FiftyFourVialPlate, Plate, Letter, Num
from tests.constants import *


class TestInj(unittest.TestCase):
    def setUp(self):
        path_constants = room(242)
        for path in path_constants:
            if not os.path.exists(path):
                self.fail(
                    f"{path} does not exist on your system. If you would like to run tests, please change this path.")

        self.hplc_controller = HPLCController(comm_dir=path_constants[0],
                                              method_dir=path_constants[1],
                                              data_dir=path_constants[2],
                                              sequence_dir=path_constants[3])

    def test_load_inj(self):
        self.hplc_controller.switch_method(DEFAULT_METHOD)
        try:
            self.hplc_controller.load_injector_program()
        except Exception as e:
            self.fail(f"Should have not failed, {e}")

    def test_edit_inj(self):
        self.hplc_controller.switch_method(DEFAULT_METHOD)
        try:
            injector_program = InjectorTable(
                functions=[
                    Draw(
                        amount=0.3,
                        source=FiftyFourVialPlate(
                            plate=Plate.ONE,
                            letter=Letter.A,
                            num=Num.EIGHT)),
                    Remote(
                        command=RemoteCommand.PREPARE,
                        duration=10,
                    ),
                    Wait(
                        duration=2
                    ),
                    Inject(

                    )
                ]
            )
            self.hplc_controller.edit_injector_program(injector_program)
        except Exception as e:
            self.fail(f"Should have not failed: {e}")

    def test_edit_inj_def(self):
        self.hplc_controller.switch_method(DEFAULT_METHOD)
        try:
            injector_program = InjectorTable(
                functions=[
                    Draw(
                        amount=0.3,
                        source=FiftyFourVialPlate(
                            plate=Plate.ONE,
                            letter=Letter.A,
                            num=Num.EIGHT)),
                    Inject(

                    )
                ]
            )

            self.hplc_controller.edit_injector_program(injector_program)
        except Exception as e:
            self.fail(f"Should have not failed: {e}")


if __name__ == '__main__':
    unittest.main()
