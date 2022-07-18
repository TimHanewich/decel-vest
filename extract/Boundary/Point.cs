using System;

namespace extract.Boundary
{
    public class Point
    {
        public float X {get; set;}
        public float Y {get; set;}

        public Point()
        {

        }

        public Point(float x, float y)
        {
            X = x;
            Y = y;
        }

        public static Point Parse(string s)
        {
            try
            {
                string[] parts = s.Split(",", StringSplitOptions.RemoveEmptyEntries);
                Point p = new Point();
                p.X = Convert.ToSingle(parts[0]);
                p.Y = Convert.ToSingle(parts[1]);
                return p;
            }
            catch (Exception ex)
            {
                throw new Exception("Unable to parse '" + s + "' into Point: " + ex.Message);
            }
        }

        // Borrowed from "M Katz": https://stackoverflow.com/questions/217578/how-can-i-determine-whether-a-2d-point-is-within-a-polygon#:~:text=Compute%20the%20oriented%20sum%20of,degrees%2C%20the%20point%20is%20inside.
        public static bool IsPointInPolygon( Point p, Point[] polygon )
        {
            double minX = polygon[ 0 ].X;
            double maxX = polygon[ 0 ].X;
            double minY = polygon[ 0 ].Y;
            double maxY = polygon[ 0 ].Y;
            for ( int i = 1 ; i < polygon.Length ; i++ )
            {
                Point q = polygon[ i ];
                minX = Math.Min( q.X, minX );
                maxX = Math.Max( q.X, maxX );
                minY = Math.Min( q.Y, minY );
                maxY = Math.Max( q.Y, maxY );
            }

            if ( p.X < minX || p.X > maxX || p.Y < minY || p.Y > maxY )
            {
                return false;
            }

            // https://wrf.ecse.rpi.edu/Research/Short_Notes/pnpoly.html
            bool inside = false;
            for ( int i = 0, j = polygon.Length - 1 ; i < polygon.Length ; j = i++ )
            {
                if ( ( polygon[ i ].Y > p.Y ) != ( polygon[ j ].Y > p.Y ) &&
                    p.X < ( polygon[ j ].X - polygon[ i ].X ) * ( p.Y - polygon[ i ].Y ) / ( polygon[ j ].Y - polygon[ i ].Y ) + polygon[ i ].X )
                {
                    inside = !inside;
                }
            }

            return inside;
        }
    }
}