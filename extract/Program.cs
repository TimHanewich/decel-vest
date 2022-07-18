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
            Point p1 = new Point();
            p1.X = 27.207793f;
            p1.Y = -82.451598f;
            Point p2 = new Point();
            p2.X = 27.207680f;
            p2.Y = -82.451278f;
            Point p3 = new Point();
            p3.X = 27.207965f;
            p3.Y = -82.451158f;
            Point p4 = new Point();
            p4.X = 27.208071f;
            p4.Y = -82.451475f;
            List<Point> points = new List<Point>();
            points.Add(p1);
            points.Add(p2);
            points.Add(p3);
            points.Add(p4);

            Point gps = new Point();
            gps.X = 27.207865f;
            gps.Y = -82.451644f;

            bool inside = Point.IsPointInPolygon(gps, points.ToArray());
            Console.WriteLine(inside);

        }
    }
}