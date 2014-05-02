 
  
  
  
  
  
 .assembly extern mscorlib {} 
  
 .assembly hello 
 { 
 .ver 1:0:1:0 
 } 
  
 .module hello.exe 
  
 .method static void main() cil managed 
 { 
 .maxstack 2 
 .entrypoint 
  
 .locals init (int32 a, int32 b) 
  
 .line 23  ldstr  "Input positive x: "  
         call void [mscorlib]System.Console::Write (string)   
 .line 24  call string [mscorlib]System.Console::ReadLine ()  
 .line 25  call int32 [mscorlib]System.Int32::Parse(string)  
 .line 26  stloc a  
 .line 27  ldloc a
	ldc.i4.s 0
	cgt  
 .line 28  brfalse.s not_so_12
		ldstr  "It is positive!\n"  
         call void [mscorlib]System.Console::Write (string)   ldc.i4.s 2  stloc b ldstr  "x * 2 = "  
         call void [mscorlib]System.Console::Write (string)   ldloc a   ldloc b  mul call void [mscorlib]System.Console::Write (int32) ldstr  ""  
         call void [mscorlib]System.Console::WriteLine (string) 
	br.s done_12
	not_so_12:
		ldstr  "It isn't positive.\n"  
         call void [mscorlib]System.Console::Write (string) 
	done_12:  
 .line 45  call string [mscorlib]System.Console::ReadLine ()  
 .line 46  ret  
 }
