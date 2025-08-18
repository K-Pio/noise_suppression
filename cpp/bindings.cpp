#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "acoustics.hpp"

namespace py = pybind11;

PYBIND11_MODULE(acoustics_c, m) 
{
      m.doc() = "C++ acoustics helpers ...";

      m.def("gain_distance", &acoustics::gain_distance,
            py::arg("r"), py::arg("r0"), py::arg("rmax"), py::arg("gmin") = 0.02,
            "Distance attenuation with floor and max range.");

      m.def("pan_lr", &acoustics::pan_lr,
            py::arg("src_x"), py::arg("lst_x"), py::arg("R"),
            "Equal-power stereo panning based on horizontal offset.");

      m.def("intersects", &acoustics::intersects,
            py::arg("ax"), py::arg("ay"), py::arg("bx"), py::arg("by"),
            py::arg("cx"), py::arg("cy"), py::arg("dx"), py::arg("dy"),
            "Segment-segment intersection test.");

      m.def("smooth", &acoustics::smooth,
            py::arg("prev"), py::arg("target"), py::arg("alpha"),
            "Smoothness.");

      m.def("smooth_channels", &acoustics::smooth_channels,
            py::arg("channels"), py::arg("targets"), py::arg("alpha"),
            "Smoothness but channels.");
      
      m.def("dist", &acoustics::dist,
            py::arg("a"), py::arg("b"),
            "Euclidean distance between two Vec2.");
      
      m.def("dist", &acoustics::dist_tuple,
            py::arg("a"), py::arg("b"),
            "dist tuple");  // override


}
