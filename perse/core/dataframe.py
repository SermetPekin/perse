"""
MIT License
Package: perse
Copyright (c) 2024 Sermet Pekin

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


from .sql_operations import SQLDataFrame
from .plotting import PlottingDataFrame
from .df_utilities import UtilitiesDataFrame
from .copy import CopyMixin

class DataFrame(SQLDataFrame, PlottingDataFrame, UtilitiesDataFrame, CopyMixin):
    def final_init(self, *args, **kwargs):
        """final_init"""
        super().__init__(*args, **kwargs)
        _ = self.get_table_name()
        return self


    def final_copy(self, *args, **kwargs):
        """final_init"""
        return self.__class__(dl= kwargs['dl'])
