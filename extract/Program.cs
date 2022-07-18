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

            Point[][]? points = JsonSerializer.Deserialize<Point[][]>(System.IO.File.ReadAllText(@"C:\Users\tahan\Downloads\polygons.json"));
            if (points != null)
            {
                Point p = Point.Parse("27.207639, -82.451911");
                bool i = Point.IsPointInPolygon(p, points[0]);
                Console.WriteLine(i);
            }

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