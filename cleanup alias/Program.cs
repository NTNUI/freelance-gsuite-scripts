using Newtonsoft.Json;

namespace Cleanup
{
    public static class Program
    {
        public static async Task Main()
        {
            while (true)
            {
                string what = Ask("What do you want to do? \n \"alias\" -> to check alias \n \"slack\" -> to check slack");
                if (what == "slack")
                    await CheckSlack();
                else if (what == "alias")
                    await CheckAliases();
                Console.WriteLine("Done! \n\n");
            }
        }

        public static string Ask(string text)
        {
            Console.WriteLine(text);
            return Console.ReadLine();
        }

        public static async Task CheckSlack()
        {
            List<User> slackUsers = await ReadFile<User>("./slackusers.json");
            List<User> users = await ReadFile<User>("./users.json");
            List<Member> members = await ReadFile<Member>("./members.json");
            members = members.Where(m => m.Role.ToLower() != "member").ToList();

            List<string> output = new List<string>();
            foreach (var slackUser in slackUsers)
            {
                var user = users.FirstOrDefault(m => m.Mail == slackUser.Mail);
                if (user == null || !members.Any(m => m.Name == user.Name))
                    output.Add($"{slackUser.Name} ---- {slackUser.Mail}");
            }

            await System.IO.File.WriteAllLinesAsync("./slackresult.json", output);
        }
        public static async Task CheckAliases()
        {
            List<Alias> aliases = await ReadFile<Alias>("./aliases.json");
            List<Member> members = await ReadFile<Member>("./members.json");
            List<User> users = await ReadFile<User>("./users.json");

            List<string> membersWithoutAlias = new();

            foreach (var member in members)
            {
                var user = users.FirstOrDefault(m => m.Name == member.Name);
                if (user == null)
                {
                    membersWithoutAlias.Add("Fant ikke bruker: " + member.Name);
                    continue;
                }
                var alias = aliases.Where(m => m.OriginalMail == user.Mail).ToList();

                if (member.Role == "Leader")
                {
                    if (!alias.Any() || !alias.Any(m => m.AliasText.Contains("leder@")))
                        membersWithoutAlias.Add(member.Gruppe + " - leder - " + member.Name);
                }
                else if (member.Role == "Deputy Leader")
                {
                    if (!alias.Any() || !alias.Any(m => m.AliasText.Contains("nestleder@")))
                        membersWithoutAlias.Add(member.Gruppe + " - nestleder - " + member.Name);
                }
                else if (member.Role == "Cashier")
                    if (!alias.Any() || !alias.Any(m => m.AliasText.Contains("kasserer@")))
                        membersWithoutAlias.Add(member.Gruppe + " - kasserer - " + member.Name);
            }

            await System.IO.File.WriteAllLinesAsync("./aliasresult.json", membersWithoutAlias);
        }
        public static async Task<List<T>> ReadFile<T>(string path)
        {
            var text = await System.IO.File.ReadAllTextAsync(path);
            return JsonConvert.DeserializeObject<List<T>>(text);
        }
    }
}