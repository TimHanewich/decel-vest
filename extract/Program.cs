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

            List<Point> points = new List<Point>();
            points.Add(Point.Parse("27.165232, -82.458301"));
            points.Add(Point.Parse("27.165232, -82.458301"));
            points.Add(Point.Parse("27.163361, -82.458677"));
            points.Add(Point.Parse("27.163361, -82.458677"));
            points.Add(Point.Parse("27.159291, -82.459620"));
            points.Add(Point.Parse("27.159084, -82.459645"));
            points.Add(Point.Parse("27.157131, -82.459588"));
            points.Add(Point.Parse("27.155394, -82.460143"));
            points.Add(Point.Parse("27.154569, -82.461009"));
            points.Add(Point.Parse("27.155135, -82.461520"));
            points.Add(Point.Parse("27.167604, -82.461492"));
            

            Console.WriteLine(JsonSerializer.Serialize(points.ToArray()));

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