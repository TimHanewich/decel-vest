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
            points.Add(Point.Parse("27.207955, -82.455660"));
            points.Add(Point.Parse("27.208937, -82.454795"));
            points.Add(Point.Parse("27.208630, -82.451515"));
            points.Add(Point.Parse("27.209575, -82.449498"));
            points.Add(Point.Parse("27.210023, -82.445249"));
            points.Add(Point.Parse("27.208487, -82.443983"));
            points.Add(Point.Parse("27.200403, -82.442049"));
            points.Add(Point.Parse("27.200479, -82.446770"));
            points.Add(Point.Parse("27.202805, -82.447825"));
            points.Add(Point.Parse("27.203718, -82.448206"));
            points.Add(Point.Parse("27.203906, -82.448469"));
            points.Add(Point.Parse("27.204538, -82.449429"));
            points.Add(Point.Parse("27.206050, -82.452354"));
            points.Add(Point.Parse("27.207363, -82.451920"));
            points.Add(Point.Parse("27.207476, -82.452239"));
            points.Add(Point.Parse("27.206152, -82.452833"));
            points.Add(Point.Parse("27.207280, -82.455212"));
            points.Add(Point.Parse("27.207955, -82.455660"));

            Console.WriteLine(JsonSerializer.Serialize(points.ToArray()));

            Point p = Point.Parse("27.207639, -82.451911");

            bool i = Point.IsPointInPolygon(p, points.ToArray());
            Console.WriteLine(i);

        }
    }
}