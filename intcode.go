package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"strconv"
	"strings"
	"time"
)

var mode0, mode1, mode2 []uint8

func init() {
	mode0 = make([]uint8, 0x8000)
	mode1 = make([]uint8, 0x8000)
	mode2 = make([]uint8, 0x8000)
	for i := range mode0 {
		mode0[i] = uint8((i / 100) % 10)
		mode1[i] = uint8((i / 1000) % 10)
		mode2[i] = uint8((i / 10000) % 10)
	}
}

type Machine struct {
	RAM []int64
	In  []int64
	Out []int64
	IP  int64
	RB  int64
}

func NewMachine(program, in []int64) *Machine {
	m := Machine{}
	m.RAM = make([]int64, 0xffff)
	for i, x := range program {
		m.RAM[i] = x
	}
	m.In = in
	return &m
}

func (m *Machine) Read(mode, i int64) int64 {
	switch mode {
	case 0:
		return m.RAM[i]
	case 1:
		return i
	case 2:
		return m.RAM[i+m.RB]
	default:
		panic("invalid read mode")
	}
}

func (m *Machine) Write(mode, i, x int64) {
	switch mode {
	case 0:
		m.RAM[i] = x
	case 2:
		m.RAM[i+m.RB] = x
	default:
		panic("invalid write mode")
	}
}

func (m *Machine) Run() {
	for m.Step() {
	}
}

func (m *Machine) Step() bool {
	ip := m.IP
	code := m.RAM[ip]
	op := code % 100
	if op == 99 {
		return false
	}
	x := code & 0x7fff
	m0 := int64(mode0[x])
	m1 := int64(mode1[x])
	m2 := int64(mode2[x])
	a0 := m.RAM[ip+1]
	a1 := m.RAM[ip+2]
	a2 := m.RAM[ip+3]
	switch op {
	case 1:
		m.IP += 4
		x0 := m.Read(m0, a0)
		x1 := m.Read(m1, a1)
		m.Write(m2, a2, x0+x1)
	case 2:
		m.IP += 4
		x0 := m.Read(m0, a0)
		x1 := m.Read(m1, a1)
		m.Write(m2, a2, x0*x1)
	case 3:
		m.IP += 2
		x := m.In[0]
		m.In = m.In[1:]
		m.Write(m0, a0, x)
	case 4:
		m.IP += 2
		x := m.Read(m0, a0)
		m.Out = append(m.Out, x)
	case 5:
		m.IP += 3
		x0 := m.Read(m0, a0)
		x1 := m.Read(m1, a1)
		if x0 != 0 {
			m.IP = x1
		}
	case 6:
		m.IP += 3
		x0 := m.Read(m0, a0)
		x1 := m.Read(m1, a1)
		if x0 == 0 {
			m.IP = x1
		}
	case 7:
		m.IP += 4
		x0 := m.Read(m0, a0)
		x1 := m.Read(m1, a1)
		if x0 < x1 {
			m.Write(m2, a2, 1)
		} else {
			m.Write(m2, a2, 0)
		}
	case 8:
		m.IP += 4
		x0 := m.Read(m0, a0)
		x1 := m.Read(m1, a1)
		if x0 == x1 {
			m.Write(m2, a2, 1)
		} else {
			m.Write(m2, a2, 0)
		}
	case 9:
		m.IP += 2
		x := m.Read(m0, a0)
		m.RB += x
	}
	return true
}

func Run(program, in []int64) []int64 {
	m := NewMachine(program, in)
	m.Run()
	return m.Out
}

func main() {
	args := os.Args[1:]
	if len(args) != 1 {
		log.Fatal("invalid arguments")
	}

	bytes, err := ioutil.ReadFile(args[0])
	if err != nil {
		log.Fatal(err)
	}

	line := strings.TrimSpace(string(bytes))
	tokens := strings.Split(line, ",")
	program := make([]int64, len(tokens))
	for i, token := range tokens {
		program[i], _ = strconv.ParseInt(token, 10, 64)
	}

	start := time.Now()
	fmt.Println(Run(program, []int64{1}))
	fmt.Println(Run(program, []int64{2}))
	fmt.Println(time.Since(start))
}
