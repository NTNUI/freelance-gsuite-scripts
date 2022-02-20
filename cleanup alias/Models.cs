public class Alias
{
    public string Name { get; set; }
    public string AliasText { get; set; }
    public string OriginalMail { get; set; }
}

public class Member
{
    public int Id { get; set; }
    public string Role { get; set; }
    public string Name { get; set; }
    public string Gruppe { get; set; }
}

public class User
{
    public string Name { get; set; }
    public string Mail { get; set; }
}