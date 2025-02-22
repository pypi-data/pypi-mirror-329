import os
import unittest

import sbol3
import rdflib


MODULE_LOCATION = os.path.dirname(os.path.abspath(__file__))
SBOL3_LOCATION = os.path.join(MODULE_LOCATION, 'SBOLTestSuite', 'SBOL3')


class TestReferencedObject(unittest.TestCase):

    def setUp(self) -> None:
        sbol3.set_defaults()

    def tearDown(self) -> None:
        sbol3.set_defaults()

    def test_list_property_reference_counter(self):
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        doc = sbol3.Document()
        component = sbol3.Component('c1', sbol3.SBO_DNA)

        # Test that the reference counter is initialized
        seq1 = sbol3.Sequence('seq1')
        self.assertListEqual(seq1._references, [])
        doc.add(component)
        doc.add(seq1)
        
        # Test that the reference counter is working
        component.sequences = [seq1.identity]
        self.assertListEqual(seq1._references, [component])

        # Test that the reference counter is cleared
        component.sequences = []
        self.assertListEqual(seq1._references, [])

        # Test that the reference counter works with the append method
        component.sequences.append(seq1.identity)
        self.assertListEqual(seq1._references, [component])

        # Test that the reference counter is cleared
        component.sequences.remove(seq1)
        self.assertListEqual(seq1._references, [])

    def test_singleton_property_reference_counter(self):
        sbol3.set_namespace('https://github.com/synbiodex/pysbol3')
        doc = sbol3.Document()
        root = sbol3.Component('root', sbol3.SBO_DNA)
        sub = sbol3.Component('sub', sbol3.SBO_DNA)

        doc.add(root)
        doc.add(sub)

        feature = sbol3.SubComponent(instance_of=root)
        root.features.append(feature)
        self.assertEqual(root._references, [feature])
        


if __name__ == '__main__':
    unittest.main()
