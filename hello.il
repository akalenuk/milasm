 
 
 
 
 
.assembly extern mscorlib {} 
 
.assembly hello 
{ 
.ver 1:0:1:0 
} 
.module hello.exe 
 
 
.method public static int32 MulInt32 (int32 a, int32 b) cil managed 
{ 
.maxstack 2 
 
.line 19 ldarg a 
.line 20 ldarg b 
.line 21 mul 
 
.line 23 ret 
} 
 
.method static void main() cil managed 
{ 
.maxstack 2 
.entrypoint 
 
.locals init (int32 a, int32 b) 
 
.line 33  ldstr "Input positive x: " 
	call void [mscorlib]System.Console::Write (string)  
.line 34  call string [mscorlib]System.Console::ReadLine ()  
.line 35  call int32 [mscorlib]System.Int32::Parse(string)  
.line 36 dup 
.line 37 stloc a 
.line 38 ldc.i4.s 0 
.line 39 cgt 
.line 40  brfalse.s not_so_5
	ldstr "Yes!\n" 
	call void [mscorlib]System.Console::Write (string)
	not_so_5:  
 
.line 42 ldc.i4.s 2 
.line 43 stloc b 
 
.line 45 ldstr  "x * 2 = "  
.line 46  call void [mscorlib]System.Console::Write (string)  
 
.line 48 ldloc a 
.line 49 ldloc b 
.line 50 call int32 MulInt32 (int32, int32) 
.line 51  call void [mscorlib]System.Console::Write (int32)  
 
.line 53 ldstr  ""  
.line 54  call void [mscorlib]System.Console::WriteLine (string)  
.line 55  call string [mscorlib]System.Console::ReadLine ()  
 
.line 57 ret 
}
