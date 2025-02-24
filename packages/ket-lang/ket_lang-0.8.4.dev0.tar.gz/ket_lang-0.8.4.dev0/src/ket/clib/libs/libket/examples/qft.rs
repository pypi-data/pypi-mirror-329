// SPDX-FileCopyrightText: 2024 Evandro Chagas Ribeiro da Rosa <evandro@quantuloop.com>
//
// SPDX-License-Identifier: Apache-2.0

use std::f64::consts::PI;

use ket::{execution::LogicalQubit, prelude::*};

fn qft(process: &mut Process, qubits: &[LogicalQubit], do_swap: bool) -> Result<(), KetError> {
    if qubits.len() == 1 {
        return process.gate(QuantumGate::Hadamard, qubits[0]);
    }

    let init = &qubits[..qubits.len() - 1];
    let last = qubits[qubits.len() - 1];
    process.gate(QuantumGate::Hadamard, last)?;
    for (i, c) in init.iter().enumerate() {
        c1gate(
            process,
            QuantumGate::Phase(PI / 2.0_f64.powi(i as i32 + 1)),
            *c,
            last,
        )?;
    }
    qft(process, init, false)?;

    if do_swap {
        for i in 0..qubits.len() / 2 {
            swap(process, qubits[i], qubits[qubits.len() - i - 1])?;
        }
    }

    Ok(())
}

fn main() -> Result<(), KetError> {
    let config = Configuration {
        num_qubits: 12,
        qpu: Some(QPU::new(
            // 0--1--2--3
            // |  |  |  |
            // 4--5--6--7
            // |  |  |  |
            // 8--9--A--B
            Some(ket::ex_arch::GRID12.to_vec()),
            12,
            U2Gates::RzSx,
            U4Gate::CX,
        )),
        ..Default::default()
    };

    let mut process = Process::new(config);

    let size = 12;
    let qubits: Vec<_> = (0..size).map(|_| process.alloc().unwrap()).collect();

    qft(&mut process, &qubits, true)?;

    process.transpile();

    println!("{:#?}", process.metadata());

    Ok(())
}
