using System;
using System.Collections.Generic;
using System.Text.Json;
using TimHanewich.Csv;

namespace extract
{
    public class MPU6050Log
    {
        public int Index {get; set;}
        public int Ticks {get; set;}
        public float gX {get; set;}
        public float gY {get; set;}
        public float gZ {get; set;}
        public float TempC {get; set;}

        public static MPU6050Log[] Extract(string log_txt)
        {
            int i = 0;
            string[] lines = log_txt.Split("\n");
            List<MPU6050Log> ToReturn = new List<MPU6050Log>();
            foreach (string line in lines)
            {
                try
                {
                    string[] parts = line.Split("_");
                    MPU6050Log l = new MPU6050Log();
                    l.Ticks = Convert.ToInt32(parts[0]);
                    l.gX = Convert.ToSingle(parts[1]);
                    l.gY = Convert.ToSingle(parts[2]);
                    l.gZ = Convert.ToSingle(parts[3]);
                    l.TempC = Convert.ToSingle(parts[4]);
                    l.Index = i;
                    ToReturn.Add(l);
                    i = i + 1;
                }
                catch
                {

                }
            }
            return ToReturn.ToArray();
        }
    
        public float GForce()
        {
            float gf = Convert.ToSingle(Math.Sqrt((gX * gX) + (gY * gY) + (gZ * gZ)));
            return gf;
        }
    
        public Attitude ToAttitude()
        {
            Attitude ToReturn = new Attitude();

            //Calculate in ms2:
            float ms2_x = gX * 9.80665f;
            float ms2_y = gY * 9.80665f;
            float ms2_z = gZ * 9.80665f;

            //Calculate pitch - rads
            double tdb = Math.Sqrt((ms2_y * ms2_y) + (ms2_z * ms2_z));
            if (tdb == 0)
            {
                return ToReturn;
            }
            double pitch_rads = Math.Atan(ms2_x / tdb);

            //Calculate roll - rads
            tdb = Math.Sqrt((ms2_x * ms2_x) + (ms2_z * ms2_z));
            if (tdb == 0)
            {
                return ToReturn;
            }
            double roll_rads = Math.Atan(ms2_y / tdb);

            //Convert
            double pitch_degs = pitch_rads * (180 / Math.PI);
            double roll_degs = roll_rads * (180 / Math.PI);

            ToReturn.Pitch = Convert.ToSingle(pitch_degs);
            ToReturn.Roll = Convert.ToSingle(roll_degs);
            return ToReturn;
        }

        public static string ToCSV(MPU6050Log[] logs)
        {
            CsvFile csv = new CsvFile();
            
            //Add the header row
            DataRow h = csv.AddNewRow();
            h.Values.Add("Index");
            h.Values.Add("Ticks");
            h.Values.Add("gX");
            h.Values.Add("gY");
            h.Values.Add("gZ");
            h.Values.Add("TempC");
            h.Values.Add("GForce");
            h.Values.Add("Pitch");
            h.Values.Add("Roll");

            //Add each row
            foreach (MPU6050Log log in logs)
            {
                DataRow dr = csv.AddNewRow();
                dr.Values.Add(log.Index.ToString());
                dr.Values.Add(log.Ticks.ToString());
                dr.Values.Add(log.gX.ToString());
                dr.Values.Add(log.gY.ToString());
                dr.Values.Add(log.gZ.ToString());
                dr.Values.Add(log.TempC.ToString());
                dr.Values.Add(log.GForce().ToString());
                dr.Values.Add(log.ToAttitude().Pitch.ToString());
                dr.Values.Add(log.ToAttitude().Roll.ToString());
            }

            return csv.GenerateAsCsvFileContent();
        }

    }
}