using System;
using System.Text.Json;
using System.Collections.Generic;
using extract.Boundary;

namespace extract
{
    public class Program
    {

        public static void Main(string[] args)
        {

            CompilePolygons();

        }

        public static void CompilePolygons()
        {
            List<Point[]> areas = new List<Point[]>();
            string[] paths = System.IO.Directory.GetFiles(@"C:\Users\tahan\Downloads\decel-vest\polygons\polygons");
            foreach (string path in paths)
            {
                string content = System.IO.File.ReadAllText(path);
                Point[]? points = JsonSerializer.Deserialize<Point[]>(content);
                if (points != null)
                {
                    areas.Add(points);
                }
            }
            Console.WriteLine(JsonSerializer.Serialize(areas));
        }

    }
}