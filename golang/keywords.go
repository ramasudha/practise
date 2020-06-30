package main

import "fmt"
import (
	"math"
	"math/cmplx"
	"runtime"
)

// A var statement can be at package or function level
var test bool

// A var declaration can include initializers, one per variable.
var i, j int = 10, 11
//If an initializer is present, the type can be omitted; the variable will take the type of the initializer.
var golang, python = true, false

var (
	ToBe   bool       = false
	MaxInt uint64     = 1<<64 - 1
	z      complex128 = cmplx.Sqrt(-5 + 12i)
)

const Pi = 3.14

// short hand notation of the function arguments
func add(x, y int) int {
	return x + y
}

// swap function
func swap(x, y string) (string, string) {
	return y, x
}


// A return statement without arguments returns the named return values. This is known as a "naked" return.
func split(sum int) (x, y int) {
	x = sum * 4 / 9
	y = sum - x
	return
}

func sum(){
	sum := 0
	for i := 0; i < 10; i++ {
		sum += i
	}
	fmt.Println(sum)
	sum = 1
	for {
		sum += sum
		if sum == 8 {
			break
		}
	}
	fmt.Println(sum)
	for sum < 16 {
		sum += sum
	}
	fmt.Println(sum)
}

func pow(x, n, lim float64) float64 {
	// Variables declared by the statement are only in scope until the end of the if.
	if v := math.Pow(x, n); v < lim {
		return v
	} else { // Variables declared inside an if short statement are also available inside any of the else blocks.
		fmt.Printf("%g >= %g\n", v, lim)
	}
	return lim
}

func switch_func() {
	fmt.Print("Go runs on ")
	switch os := runtime.GOOS; os {
	case "darwin":
		fmt.Println("OS X.")
	case "linux":
		fmt.Println("Linux.")
	default:
		// freebsd, openbsd,
		// plan9, windows...
		fmt.Printf("%s.\n", os)
	}
}

func defer_test() {
	// A defer statement defers the execution of a function until the surrounding function returns.
	// The deferred call's arguments are evaluated immediately,
	//  but the function call is not executed until the surrounding function returns.
	defer fmt.Println("worjhd")

	fmt.Println("hello")
	// Deferred function calls are pushed onto a stack. When a function returns,
	// its deferred calls are executed in last-in-first-out order.
	for i := 0; i < 3; i++ {
		defer fmt.Println(i)
	}

	fmt.Println("done")
}

func main(){
	var test int
	fmt.Println("test", math.Pi, add(1,2))
	b, a := swap("1","2")
	fmt.Println("swap", b, a)
	fmt.Println(split(17))
	fmt.Println(test, i, j, golang, python)
	fmt.Printf("Type: %T Value: %v\n", ToBe, ToBe)
	fmt.Printf("Type: %T Value: %v\n", MaxInt, MaxInt)
	fmt.Printf("Type: %T Value: %v\n", z, z)
	fmt.Println(Pi)
	sum()
	fmt.Println(pow(5,5,3))
	switch_func()
	defer_test()
}
