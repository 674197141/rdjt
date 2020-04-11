package main

import (
	"fmt"
	"log"
	"os"
)

func main() {
	Create_file("test.txt")
	Read_file("test.txt")
}

func Read_file(file_name string){
	var (
		currFile *os.File
		err error
	)
	currFile,err = os.Open(file_name)
	if err != nil {
		log.Fatal(err)
	}
	defer currFile.Close()
	buf := make([]byte,1024)
	for  {
		n,_:=currFile.Read(buf)
		if 0==n {
			break
		}
		os.Stdout.Write(buf[:n])
	}
}


func Create_file(file_name string)  {
	var (
		newFile *os.File
		err error
	)
	newFile, err = os.Create(file_name)
	if err != nil {
		log.Fatal(err)
	}
	byteSlice := []byte("abc\n")
	bytesWritten, err := newFile.Write(byteSlice)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println("Wrote %d bytes.\n", bytesWritten)
	fmt.Println(newFile)
	newFile.Close()
}

func Zhuce(){

}

func Login() {

}
