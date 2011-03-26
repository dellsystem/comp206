/*-----------------------------------------------------------------
*  LiteClockApp 1.0.
*  Author:  Ivan 'MCG' Boldyrev <bii714@cclib.nsu.ru>
*       http://members.tripod.com/~ivan_mcg/    (Eng)
*       http://www.halyava.ru/applet/           (Rus)
*------------------------------------------------------------------
*   This is a last comment in this file. I have no own computer,
* and I have no time to comment my programs. I am sorry.
*----------------------------------------------------------------*/

import java.awt.*;
import java.util.Date;
import java.util.StringTokenizer;

final public class LiteClockApp extends java.applet.Applet implements Runnable
{  volatile boolean over, md;
   long startTime=System.currentTimeMillis()<<1;
   Image buff;
   Dimension oldSz;
   Color fore, back, shad;
   int dateVSize, countMode, drawMode, transMode;
   final int[] on=new int[6], newb=new int[6], onf=new int[6], was=new int[6];
   final static int COLSIZE=150;///
   final Color[] colTab=new Color[COLSIZE];
   volatile int ms;

   public String getAppletInfo()
   {  return "LiteClock v1.0. Author: Ivan Boldyrev <bii714@cclib.nsu.ru>\n"
         +"http://members.tripod.com/~ivan_mcg\t(Eng)\n"
         +"http://www.halyava.ru/applet\t\t(Rus)";
   }

   private static final int font[]={ 0x3F, 0x18, 0x76, 0x7C, 0x59, 0x6D, 0x6F,
         0x38, 0x7F, 0x7D };

   private static final String days[]={ "Sun", "Mon", "Tue", "Wed", "Thu",
         "Fri", "Sat" };

   final void drawSymbol(Graphics gr, int ind, int x, int y, int h)
   {  int d, x2, x3, r;
      r=h>>2;
      switch (drawMode & 0x0F)
      {  default:
         case 0:
            x3=x2=x;
            break;
         case 1:
            d=h>>3;
            x2=x+d;
            x3=x-d;
            break;
         case 2:
            x3=x2=x+(h>>3);
            break;
         case 3:
            x3=x2=x-(h>>3);
            break;
      }

      int map=1, now=on[ind], fresh=newb[ind], ww=was[ind];
      int s=(ms*255)/1000;
      Color col;
      for (int count=0 ; count<7;  map<<=1, ++count)
      {  if ((map & now)!=0)
            col=(s>=COLSIZE || 0==(fresh & map)) ? fore : colTab[s];
	 else
            col=((map & ww)!=0 && s<COLSIZE) ? colTab[COLSIZE-1-s] : shad;
	 gr.setColor(col);
         switch (count)
         {  case 0:
               drawVLine(gr, x2, y, x, h);
               break;
            case 1:
               drawVLine(gr, x, y+h, x3, h);
               break;
            case 2:
               drawHLine(gr, x3, y+h+h, h);
               break;
            case 3:
               drawVLine(gr, x+h, y+h, x3+h, h);
               break;
            case 4:
               drawVLine(gr, x2+h, y, x+h, h);
               break;
            case 5:
               drawHLine(gr, x2, y, h);
               break;
            case 6:
               drawHLine(gr, x, y+h, h);
        }
      }
   }

   final private void drawVLine(Graphics gr, int x1, int y, int x2, int h)
   {  int d=h>>3;
      int yy=y+d, hh=h-d-d;
      int[] xp=new int[7], yp=new int[7];
      xp[6]=xp[0]=x1; yp[6]=yp[0]=yy;
      xp[1]=x1-d; yp[1]=yy+d;
      xp[2]=x2-d; yp[2]=yy+hh-d;
      xp[3]=x2; yp[3]=yy+hh;
      xp[4]=x2+d; yp[4]=yy+hh-d;
      xp[5]=x1+d; yp[5]=yy+d;
      gr.fillPolygon(xp, yp, 6);
   }

   final static private void drawHLine(Graphics gr, int x, int y, int w)
   {  int d=w>>3;
      int xx=x+d, ww=w-d-d;
      int[] xp=new int[7], yp=new int[7];
      xp[6]=xp[0]=xx; yp[6]=yp[0]=y;
      xp[1]=xx+d; yp[1]=y-d;
      xp[2]=xx+ww-d; yp[2]=y-d;
      xp[3]=xx+ww; yp[3]=y;
      xp[4]=xx+ww-d; yp[4]=y+d;
      xp[5]=xx+d; yp[5]=y+d;
      gr.fillPolygon(xp, yp, 7);
   }

   public void init()
   {  Font f=new Font("Courier", Font.BOLD, 20);
      FontMetrics fm=getFontMetrics(f);
      dateVSize=10+fm.getHeight();
      setFont(f);
   }


   public void start()
   {  fore=parceColor(getParameter("FORE"), Color.green);
      back=parceColor(getParameter("BACK"), Color.black);
      shad=parceColor(getParameter("SHAD"), darkColor(fore, back));
      try
      {  drawMode=Integer.parseInt(getParameter("MODE"), 16);
      }
      catch (Exception ex)
      {  drawMode=0;
      }
      try
      {  transMode=Integer.parseInt(getParameter("TRANS"), 16);
      }
      catch (Exception ex)
      {  transMode=0;
      }
      String mod=getParameter("COUNTMODE");
      countMode=(mod!=null && mod.length()==1) ? mod.charAt(0)-'0' : 0;
      initColTab();
      over=false;
      (new Thread(this)).start();
   }

   public void run()
   {  Graphics gr=getGraphics();
      long old=System.currentTimeMillis();
      Date time=new Date();
      try
      {  while (!over)
         {  long tm=System.currentTimeMillis();
            ms=(int)(tm%1000);
            if ((tm-=ms)-old>=1000)
            {  old=tm;
               switch (countMode)
               {  default:
                  case 0:
                     time = new Date();
                     break;
                  case 1:
                     time = new Date(startTime - System.currentTimeMillis());
                     break;
               }
               onf[0]=font[time.getHours()/10];
               onf[1]=font[time.getHours()%10];
               onf[2]=font[time.getMinutes()/10];
               onf[3]=font[time.getMinutes()%10];
               onf[4]=font[time.getSeconds()/10];
               onf[5]=font[time.getSeconds()%10];
               for (int i=0; i<6; i++)
               {  newb[i]=~on[i] & onf[i];
		  was[i]=on[i] & ~onf[i];
                  on[i]=onf[i];
               }
            }
            md=650<ms;
            paint(gr);
            Thread.yield();
         }
      }
      finally
      {  gr.dispose();
      }
   }

   public void stop()
   {  over=true;
   }

   public void update(Graphics g)
   {  paint(g);
   }

   public void paint(Graphics g)
   {  Dimension s=size();
      int h=Math.min(s.width/12, s.height/3);
      if (buff==null || s.width!=oldSz.width || s.height!=oldSz.height)
      {  buff=null;
         System.gc();
         buff=createImage(s.width, s.height);
         oldSz=s;
      }
      Graphics bGr=buff.getGraphics();
      bGr.setColor(back);
      bGr.fillRect(0, 0, s.width, s.height);///
      bGr.translate((oldSz.width-h*9)>>1, dateVSize);
      drawSymbol(bGr, 0, 0, h>>1, h);
      drawSymbol(bGr, 1, h+(h>>1), h>>1, h);
      drawSymbol(bGr, 2, 4*h, h>>1, h);
      drawSymbol(bGr, 3, 5*h+(h>>1), h>>1, h);
      drawSymbol(bGr, 4, 7*h, h, (h>>1)+(h>>2));
      drawSymbol(bGr, 5, 7*h+((h>>2)+h), h, (h>>1)+(h>>2));
      bGr.setColor((md) ? fore : shad);
      int r=h>>2;
      bGr.fillOval(3*h+r, h-r, r, r);
      bGr.fillOval(3*h+r, (h<<1), r, r);
      g.drawImage(buff, 0, 0, null);///
      bGr.dispose();
   }

   void initColTab()
   {  double a=Math.log(2.)/COLSIZE;
      float c;
      boolean exp=(0==(transMode&0xF0));

      if (0==(transMode&0X0F))
      {  int br=shad.getRed();
         int bg=shad.getGreen();
         int bb=shad.getBlue();
         int dr=fore.getRed()-br;
         int dg=fore.getGreen()-bg;
         int db=fore.getBlue()-bb;
         for (int n=0; n<COLSIZE; ++n)
         {  c=(exp) ? (float)Math.exp(n*a)-1 : n/(float)COLSIZE;
            colTab[n]=new Color(br+(int)(c*dr), bg+(int)(c*dg), bb+(int)(c*db));
         }
      }
      else
      {  float fr[]=Color.RGBtoHSB(fore.getRed(), fore.getGreen(),
            fore.getBlue(), null);
         float sh[]=Color.RGBtoHSB(shad.getRed(), shad.getGreen(),
            shad.getBlue(), null);
         float d0=fr[0]-sh[0], d1=fr[1]-sh[1], d2=fr[2]-sh[2];
         for (int n=0; n<COLSIZE; ++n)
         {  c=(exp) ? (float)Math.exp(a*n)-1 : n/(float)COLSIZE;
            colTab[n]=new Color(Color.HSBtoRGB(sh[0]+c*d0, sh[1]+c*d1,
                  sh[2]+c*d2) | 0xFF000000);
         }
      }
   }

   final static private Color parceColor(String src, Color def)
   {  if (src==null || src.length()<2)
         return def;
      try
      {  if (src.charAt(0)=='#')
            return new Color(Integer.parseInt(src.substring(1), 16)
                  | 0xFF000000);
         else
         {  StringTokenizer stt=new StringTokenizer(src, " ;,");
            int res=0xFF;
            for (int i=0; i<3; ++i)
            {  res <<= 8;
               res |= Integer.parseInt(stt.nextToken());
            }
            return new Color(res);
         }
      }
      catch (Exception e)
      {  return def;
      }
   }

   final static Color darkColor(Color f, Color b)
   {  int dr=f.getRed()-b.getRed(), dg=f.getGreen()-b.getGreen(),
               db=f.getBlue()-b.getBlue();
      return new Color(b.getRed()+(dr>>2), b.getGreen()+(dg>>2),
            b.getBlue()+(db>>2));
   }

   final static int sign(int x)
   {  return (x<0) ? -1 : ( (x>0) ? +1 : 0 );
   }
}
