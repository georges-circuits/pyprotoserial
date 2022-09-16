/*
 * This file is a part of the libprotoserial project
 * https://github.com/georges-circuits/libprotoserial
 * 
 * Copyright (C) 2022 Jiří Maňák - All Rights Reserved
 * For contact information visit https://manakjiri.eu/
 * 
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * any later version.
 * 
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <https://www.gnu.org/licenses/gpl.html>
 */


//#define SP_FRAGMENTATION_WARNING
//#define SP_BUFFERED_WARNING

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

#include "libprotoserial/fragmentation.hpp"
//#include "libprotoserial/protostacks.hpp"

#include <sstream>

namespace py = pybind11;


PYBIND11_MODULE(protoserial, m) 
{
    py::class_<sp::bytes>(m, "bytesbuff")
        .def(py::init([](py::bytes arg){
            return sp::bytes(std::string(arg));
        }))
        .def(py::init([](std::list<int> arg){
            sp::bytes ret(0, 0, arg.size());
            for (auto b : arg) ret.push_back((sp::byte)b);
            return ret;
        }))
        .def("size", &sp::bytes::size)
        .def("at", static_cast<sp::bytes::const_reference (sp::bytes::*)(sp::bytes::size_type) const>(&sp::bytes::at))
        .def("as_list", [](const sp::bytes &arg) {
            std::list<int> ret;
            for (auto b : arg) ret.push_back((int)b);
            return ret;
        })
        .def("__repr__", [](const sp::bytes &a) {
            std::stringstream s; s << "<bytesbuff " << a << '>';
            return s.str();
        });

    py::class_<sp::interface_identifier>(m, "interface_identifier")
        .def("__repr__", [](const sp::interface_identifier &a) {
            std::stringstream s; s << "<interface_identifier " << a << '>';
            return s.str();
        });

    py::class_<sp::uart_interface>(m, "uart_interface")
        .def(py::init<std::string, speed_t, sp::interface_identifier::instance_type, sp::interface::address_type, 
            sp::interface::address_type, sp::uint, sp::uint, sp::uint>())
        .def("main_task", static_cast<void(sp::uart_interface::*)()>(&sp::uart_interface::main_task))
        .def("on_fragment_receive", [](sp::uart_interface & obj, std::function<void(sp::fragment)> fn){
            obj.receive_event.subscribe(std::move(fn));
        })
        .def("transmit_fragment", static_cast<void(sp::uart_interface::*)(sp::fragment)>(&sp::uart_interface::transmit));

    py::class_<sp::fragment>(m, "fragment")
        .def(py::init<sp::fragment::address_type, sp::fragment::data_type>())
        .def("data", [](const sp::fragment & arg) {return sp::bytes(arg.data());})
        .def("source", &sp::fragment::source)
        .def("destination", &sp::fragment::destination)
        .def("set_destination", &sp::fragment::set_destination)
        .def("__repr__", [](const sp::fragment &a) {
            std::stringstream s; s << "<fragment " << a << '>';
            return s.str();
        });
    
    py::class_<sp::transfer_metadata>(m, "transfer_metadata")
        .def("get_id", &sp::transfer_metadata::get_id)
        .def("get_prev_id", &sp::transfer_metadata::get_prev_id)
        .def("source", &sp::transfer_metadata::source)
        .def("destination", &sp::transfer_metadata::destination)
        .def("interface_id", &sp::transfer_metadata::interface_id);

    py::class_<sp::transfer, sp::transfer_metadata>(m, "transfer")
        .def(py::init<sp::interface_identifier, sp::transfer::address_type>())
        .def(py::init<sp::interface_identifier, sp::transfer::address_type, sp::transfer::id_type>())
        .def("create_response", &sp::transfer::create_response_transfer)
        /* inherited from sp::transfer_metadata */
        .def("get_id", static_cast<sp::transfer::id_type(sp::transfer::*)() const>(&sp::transfer::get_id))
        .def("get_prev_id", static_cast<sp::transfer::id_type(sp::transfer::*)() const>(&sp::transfer::get_prev_id))
        .def("source", static_cast<sp::transfer::address_type(sp::transfer::*)() const>(&sp::transfer::source))
        .def("destination", static_cast<sp::transfer::address_type(sp::transfer::*)() const>(&sp::transfer::destination))
        .def("interface_id", static_cast<sp::interface_identifier(sp::transfer::*)() const>(&sp::transfer::interface_id))
        /* additional */
        .def("__repr__", [](const sp::transfer &a) {
            std::stringstream s; s << "<transfer " << a << '>';
            return s.str();
        })
        .def("get_data(", [](const sp::transfer &a) {
            return sp::bytes(a.data());
        })
        .def("set_data(", [](sp::transfer &a, sp::bytes data) {
            a.data() = std::move(data);
        });


    /* py::class_<sp::stack::uart_115200>(m, "uart_115200")
        .def(py::init<std::string, sp::interface_identifier::instance_type, sp::interface::address_type>())
        .def("main_task", &sp::stack::uart_115200::main_task)
        .def("transfer_receive_subscribe", &sp::stack::uart_115200::transfer_receive_subscribe)
        .def("transfer_ack_subscribe", &sp::stack::uart_115200::transfer_ack_subscribe)
        .def("transfer_transmit", &sp::stack::uart_115200::transfer_transmit)
        .def("interface_id", &sp::stack::uart_115200::interface_id)
        .def("new_transfer", [](const sp::stack::uart_115200 & arg){
            return sp::transfer(arg.interface);
        }); */

}



