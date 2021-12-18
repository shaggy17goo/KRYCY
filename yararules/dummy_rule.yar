rule Dummy
{
    strings:
        $a = "dummy"

    condition:
        $a
}
