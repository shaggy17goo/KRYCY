/*
 Test
*/
rule RogueIP
{
    strings:
        $localhost = "127.0.0.1" wide ascii

    condition:
        $localhost
}

