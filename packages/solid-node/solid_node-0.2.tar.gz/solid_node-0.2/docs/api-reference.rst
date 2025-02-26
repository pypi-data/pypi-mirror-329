
.. _api-reference:

=============
API Reference
=============

Each leaf node has a namespace property, constraining the object type that must be
returned by the render() function. All nodes can be imported directly from the `solid_node.node` namespace, for convenience.

Solid2Node
==========
.. autoclass:: solid_node.node.adapters.solid2.Solid2Node
   :members:
   :undoc-members:
   :show-inheritance:

CadQueryNode
============
.. autoclass:: solid_node.node.adapters.cadquery.CadQueryNode
   :members:
   :undoc-members:
   :show-inheritance:

OpenScadNode
============
.. autoclass:: solid_node.node.adapters.openscad.OpenScadNode
   :members:
   :undoc-members:
   :show-inheritance:

JScadNode
=========
.. autoclass:: solid_node.node.adapters.jscad.JScadNode
   :members:
   :undoc-members:
   :show-inheritance:

AssemblyNode
============
.. autoclass:: solid_node.node.assembly.AssemblyNode
   :members:
   :undoc-members:
   :show-inheritance:

FusionNode
==========
.. autoclass:: solid_node.node.fusion.FusionNode
   :members:
   :undoc-members:
   :show-inheritance:
