import unittest

from reservoir_info.bean.common.dimension import Dimension


class TestDimension(unittest.TestCase):
    def test_from_block_structured_grid(self):
        block_lines = ["DIMENS #Structured grid", "10 20 30"]
        dimens = Dimension.from_block(block_lines)
        self.assertEqual(dimens.nx, 10)
        self.assertEqual(dimens.ny, 20)
        self.assertEqual(dimens.nz, 30)
        self.assertEqual(dimens.ngrid, None)
        self.assertEqual(dimens.description, "Structured grid")


    def test_from_block_unstructured_grid(self):
        block_lines = ["DIMENS #Unstructured grid", "100"]
        dimens = Dimension.from_block(block_lines)
        self.assertEqual(dimens.nx, None)
        self.assertEqual(dimens.ny, None)
        self.assertEqual(dimens.nz, None)
        self.assertEqual(dimens.ngrid, 100)
        self.assertEqual(dimens.description, "Unstructured grid")


    def test_to_block_structured_grid(self):
        dimens = Dimension(nx=10, ny=20, nz=30, description="Structured grid")

        block_lines = dimens.to_block()
        self.assertEqual(block_lines, ["DIMENS #Structured grid", "10 20 30"])


    def test_to_block_unstructured_grid(self):
        dimens = Dimension(ngrid=100, description="Unstructured grid")

        block_lines = dimens.to_block()
        self.assertEqual(block_lines, ["DIMENS #Unstructured grid", "100"])


    def test_to_block_no_description(self):
        dimens = Dimension(nx=10, ny=20, nz=30)

        block_lines = dimens.to_block()
        self.assertEqual(block_lines, ["DIMENS", "10 20 30"])

    def test_from_block_no_description(self):
        txt = """
        DIMENS
         24 25 15
        """
        block_lines = txt.split("\n")

        dimens = Dimension.from_block(block_lines)
        self.assertEqual(dimens.nx, 24)
        self.assertEqual(dimens.ny, 25)
        self.assertEqual(dimens.nz, 15)
        self.assertEqual(dimens.ngrid, None)
        self.assertEqual(dimens.description, None)
        print(f'\n{dimens}')

if __name__ == '__main__':
    unittest.main()
