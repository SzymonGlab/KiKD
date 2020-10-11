import java.io.*;

import static java.lang.Math.log10;

public class Main {


    public static void main(String[] args) throws FileNotFoundException, IOException {
        if(args.length != 5)
            System.exit(0);
        File in = new File(args[0]);
        File out = new File(args[1]);
        int r = Integer.parseInt(args[2]);
        int g = Integer.parseInt(args[3]);
        int b = Integer.parseInt(args[4]);
        OutputStream output = new BufferedOutputStream(new FileOutputStream(out));

        byte by[] = b_to_arr(in);
        for (int i = 0; i < by.length; i++) {
            if ((i >= 18) && (i < by.length - 26)) {
                int r_v = byteToUnsignedInt(by[i]);
                int g_v = byteToUnsignedInt(by[i + 1]);
                int b_v = byteToUnsignedInt(by[i + 2]);
                System.out.println((int) (r_v / (256 / Math.pow(2, r))) * (int) (256 / Math.pow(2, r)) + (int) ((256 / Math.pow(2, r)) / 2));
                
                output.write((int) (r_v / (256 / Math.pow(2, r))) * (int) (256 / Math.pow(2, r)) + (int) ((256 / Math.pow(2, r)) / 2));
                output.write((int) (g_v / (256 / Math.pow(2, g))) * (int) (256 / Math.pow(2, g)) + (int) ((256 / Math.pow(2, g)) / 2));
                output.write((int) (b_v / (256 / Math.pow(2, b))) * (int) (256 / Math.pow(2, b)) + (int) ((256 / Math.pow(2, b)) / 2));
                i += 2;
            } else {
                output.write(by[i]);
            }
        }
        output.close();
        byte[] b2 = b_to_arr(out);
        for (int i = 0; i < 4; i++)
            mse(by, b2, i);
    }

    private static void mse(byte[] b1, byte[] b2, int x) throws IOException {
        double peak, signal, noise, mse;
        
        String color;
        signal = noise = peak = 0;
        for (int i = 0; i < b1.length; i++) {
            if ((i >= 18) && (i < b1.length - 26)) {
                int r1 = byteToUnsignedInt(b1[i + x]);
                int r2 = byteToUnsignedInt(b2[i + x]);
                signal += r1 * r2;
                noise += (r1 - r2) * (r1 - r2);
                if (peak < r1) {
                    peak = r1;
                }
                if (x != 3)
                    i += 2;

                if(x == 1){
                    // System.out.println(r2);
                }
            }
        }
        if (x == 0)
            color = "r";
        else if (x == 1)
            color = "g";
        else
            color = "b";

        if (x != 3) {
            System.out.println(noise);
            mse = noise / ((b1.length - 44) / 3); // Mean square error
            System.out.println("mse(" + color + ") = " + mse);
            System.out.println("SNR(" + color + ")= " + (signal / noise) + " (" + 10 * log10(signal / noise) + "dB)");
            System.out.println();
        } else {
            mse = noise / ((b1.length - 44));
            System.out.println("mse = " + mse);
            System.out.println("SNR = " + (signal / noise) + " (" + 10 * log10(signal / noise) + "dB)");
            System.out.println();
        }

    }

    private static byte[] b_to_arr(File file) throws FileNotFoundException, IOException {
        byte[] arr = new byte[(int) file.length()];
        try (FileInputStream fis = new FileInputStream(file)) {
            fis.read(arr);
            fis.close();
        }
        return arr;
    }

    public static int byteToUnsignedInt(byte b) {
        return b & 0xff;
    }

}