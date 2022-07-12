using System;
using System.Text.Json;

namespace extract
{
    public class Program
    {
        public static void Main(string[] args)
        {
            string content = System.IO.File.ReadAllText(@"C:\Users\tahan\Downloads\20220711 Calibration Test 2\log.txt");
            MPU6050Log[] logs = MPU6050Log.Extract(content);
            string csv = MPU6050Log.ToCSV(logs);
            System.IO.File.WriteAllText(@"C:\Users\tahan\Downloads\20220711 Calibration Test 2\log.csv", csv);
        }
    }
}