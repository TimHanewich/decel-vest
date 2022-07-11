using System;
using System.Text.Json;

namespace extract
{
    public class Program
    {
        public static void Main(string[] args)
        {
            string content = System.IO.File.ReadAllText(@"C:\Users\tahan\Downloads\20220711 Motorcycle Ride\log_adj.txt");
            MPU6050Log[] logs = MPU6050Log.Extract(content);
            Console.WriteLine(JsonSerializer.Serialize(logs));
        }
    }
}