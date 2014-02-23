import unittest
from ocgis.test.base import TestBase
from ocgis.interface.base.variable import Variable
import numpy as np
from cfunits.cfunits import Units
from ocgis.exc import NoUnitsError
from ocgis.util.units import get_are_units_equivalent, get_are_units_equal


class TestField(TestBase):
    
    def test_units_read_from_file(self):
        rd = self.test_data.get_rd('cancm4_tas')
        field = rd.get()
        self.assertEqual(field.variables['tas'].cfunits,Units('K'))
        
    def test_units_conform_from_file(self):
        rd = self.test_data.get_rd('cancm4_tas')
        field = rd.get()
        sub = field.get_time_region({'month':[5],'year':[2005]})
        sub.variables['tas'].cfunits_conform(Units('celsius'))
        self.assertAlmostEqual(sub.variables['tas'].value[:,6,:,30,64],np.ma.array([[28.2539310455]],mask=[[False]]))
        self.assertEqual(sub.variables['tas'].units,'celsius')


class TestUnits(unittest.TestCase):
    _create_dir = False
    
    def test_get_are_units_equivalent(self):
        units = [Units('celsius'),Units('kelvin'),Units('fahrenheit')]
        self.assertTrue(get_are_units_equivalent(units))
        
        units = [Units('celsius'),Units('kelvin'),Units('coulomb')]
        self.assertFalse(get_are_units_equivalent(units))
        
        units = [Units('celsius')]
        with self.assertRaises(ValueError):
            get_are_units_equivalent(units)
            
    def test_get_are_units_equal(self):
        units = [Units('celsius'),Units('kelvin'),Units('fahrenheit')]
        self.assertFalse(get_are_units_equal(units))
        
        units = [Units('celsius'),Units('celsius'),Units('celsius')]
        self.assertTrue(get_are_units_equal(units))
        
        units = [Units('celsius')]
        with self.assertRaises(ValueError):
            get_are_units_equal(units)


class TestVariableUnits(TestBase):
    _create_dir = False
    
    @property
    def value(self):
        return(np.array([5,5,5]))

    def test_as_string(self):        
        ## string-based units
        var = Variable(name='tas',units='celsius',value=self.value)
        self.assertEqual(var.units,'celsius')
        self.assertEqual(var.cfunits,Units('celsius'))
        self.assertNotEqual(var.cfunits,Units('kelvin'))
        self.assertTrue(var.cfunits.equivalent(Units('kelvin')))
    
    def test_conform(self):
        ## conversion of celsius units to kelvin
        var = Variable(name='tas',units='celsius',value=self.value)
        var.cfunits_conform(Units('kelvin'))
        self.assertNumpyAll(var.value,np.array([278.15]*3))
        self.assertEqual(var.cfunits,Units('kelvin'))
        self.assertEqual(var.units,'kelvin')
    
    def test_as_object(self):
        ## constructor with units objects v. string
        var = Variable(name='tas',units=Units('celsius'),value=self.value)
        self.assertEqual(var.units,'celsius')
        self.assertEqual(var.cfunits,Units('celsius'))
    
    def test_no_units(self):
        ## test no units
        var = Variable(name='tas',units=None,value=self.value)
        with self.assertRaises(NoUnitsError):
            var.cfunits
            
    def test_masked_array(self):
        ## assert mask is respected by inplace unit conversion
        value = np.ma.array(data=[5,5,5],mask=[False,True,False])
        var = Variable(name='tas',units=Units('celsius'),value=value)
        var.cfunits_conform(Units('kelvin'))
        self.assertNumpyAll(np.ma.array([278.15,None,278.15],mask=[False,True,False]),var.value)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
