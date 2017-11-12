import rhinoscriptsyntax as rs
import rhinoscriptsyntax as rs
import Rhino
import Nirvik_UI_Utility
import operator
import random
import math

rs.ClearCommandHistory()

####    SHAPE GRAMMAR NOTATIONS ######

site_labels=[]
canal_arrows=[]
shape_cross=[]
anno_hatch=[]

####    SHAPE GRAMMAR NOTATIONS ######



####    NEW GLOBAL VARIABLES    ######
new_all_border_crvs=[]
new_shaped_border_crvs_res_1=[]
new_shaped_border_crvs_res_2=[]
new_shaped_border_crvs_res_3=[]
border_shaped_crvs_det=[]

stage1_dummy_canal_arms=[]
####    NEW GLOBAL VARIABLES    ######



####    BEGIN GLOBAL VARIABLES    ####
diX=0
diY=0
cir=[]
geo1=100
geo2=100
geo3=100
bool_crvs=[]
temp_del_list_gen_crvs=[]
temp_del_list_gen_ini_crvs=[]       ####new
all_subdiv_crvs=[]
str_subdiv_ratio=[]
str_border_ratio=[]
temp_del_list_border=[]
temp_del_list_border_line=[]
dummy_border_crvs=[]
temp_del_list_subdiv=[]
temp_del_list_gen=[]
gen_crvs=[]
gen_crvs_ini=[]     #### new
n_crv=[]
del_crv=[]   #   tracks array ini curves in draw 
del_crvs=[]  #   tracks array in subdiv 
crv_gen_0=[] #   initial generation curves
crv_gen_1=[] #   first generation curves
crv_gen_2=[] #   second generation curves
crv_gen_3=[] #   second generation curves
crv_bor_0=[] #   initial border curve
crv_bor_1=[] #   first border curve
crv_bor_2=[] #   second border curve
temp_del_list_line_border=[]
temp_del_list_L_border=[]
canal_arms=[]
dummy_canal_arms=[]
dummy_canal_arm_pts=[]
dummy_canal_pl_crvs=[]
dummy_canal_pl_pts=[]
dummy_res_pts=[]
dummy_canal_pl_off_crvs=[]
dummy_canal_pl_off_pts=[]
canal_arm_gen_pts=[]
canal_arm_gen_crvs=[]
can_1_bounding_crv=[]
del_pts_index=[]

final_canal_sys=[]
temp_del_canal_arms=[]
canal_cen_pts=[]
shaped_border_crvs=[]
all_border_crv_pts=[]
border_crvs=[]
L_border_crvs=[]
line_border_crvs=[]
global_line_border=[]
canal_pl=[]
canal_pl_pts=[]
canal_pl_offset=[]
user_indent_points=[]
def0_canal_arm=[]#indented canal arms detail
tmp0_indent=[]#indent
tmp1_indent=[]#indent
tmp2_indent=[]#indent
tmp3_indent=[]#indent
def_canal_arms=[]
det_canal_ends=[]
line_borders_mod=[]
####    END GLOBAL VARIABLES    ####

####    BEGIN FUNCTIONS         ####

def clear_list(li):
    for i in li:
        li.remove(i)
    if(len(li)>0):
        clear_list(li)

def mid_pt(x0,y0,x1,y1):
    mid_pt=[(x0+x1)/2, (y0+y1)/2, 0]
    return mid_pt

def singleInstance(req_li):
    temp=[]
    for i in req_li:
        if(i not in temp):
            temp.append(i)
        else:
            req_li.remove(i)
            break
    req_li=[]
    req_li=temp
    return temp

def shapeCross(crv):
    try:
        crv_pts=rs.CurvePoints(rs.coercecurve(crv))
        crv_cen=rs.CurveAreaCentroid(crv)[0]
        di_pt=[]
        for i in range(len(crv_pts)-1):
            ang=rs.Angle(crv_cen,crv_pts[i])[0]
            if(ang<0):
                ang+=360
            di_pt.append([crv_pts[i],ang])
        di_ptx=sorted(di_pt, key=operator.itemgetter(1))
        for i in range(len(di_ptx)):
            #rs.AddTextDot(i,di_ptx[i][0])
            pass
        n=len(di_ptx)-1
        if(n==3):
            l1=rs.AddLine(di_ptx[0][0],di_ptx[2][0])
            l2=rs.AddLine(di_ptx[1][0],di_ptx[3][0])
        else:
            pts=[]
            for i in di_ptx:
                pts.append(i[0])
            p0=pts[0]
            pn=pts[len(pts)-1]
            di0=[]
            for i in range(1,len(pts)-1,1):
                d=rs.Distance(p0,pts[i])
                di0.append([pts[i],d])
            di0x=sorted(di0,key=operator.itemgetter(1))
            l1=rs.AddLine(p0,di0x[len(di0x)-1][0])
            di1=[]
            for i in range(1,len(pts)-2,1):
                d=rs.Distance(pn,pts[i])
                di1.append([pts[i],d])
            di1x=sorted(di1,key=operator.itemgetter(1))
            l2=rs.AddLine(pn,di1x[len(di1x)-1][0])
        k=200
        rs.ObjectColor(l1,(k,k,k))
        rs.ObjectColor(l2,(k,k,k))
        shape_cross.append(l1)
        shape_cross.append(l2)
    except:
        pass

def modulate(xpt, n, rx, ry, req, diX, diY, detail_2):
    #boolean everything and return central curve
    #rs.EnableRedraw(False)
    try:
        rs.DeleteObjects(shape_cross)
    except:
        pass
    try:
        rs.DeleteObjects(crvX)
    except:
        pass
    xx0=xpt[0]
    yy0=xpt[1]
    res=res_ratio.Value/35.0
    diX_this=(diX/5.0)*res*rx
    diY_this=(diY/5.0)*res*ry
    pt=[]
    if(req==1):
        pt.append( [ xx0-(diX_this),   yy0+(diY_this/2),  0] )  #0
        pt.append( [ xx0-(diX_this/2), yy0+(diY_this),    0] )  #1
        pt.append( [ xx0+(diX_this/2), yy0+(diY_this),    0] )  #2
        pt.append( [ xx0+(diX_this),   yy0+(diY_this/2),  0] )  #3
        pt.append( [ xx0+diX_this,     yy0-(diY_this/2),  0] )  #4
        pt.append( [ xx0+(diX_this/2), yy0-(diY_this),    0] )  #5
        pt.append( [ xx0-(diX_this/2), yy0-(diY_this),    0] )  #6
        pt.append( [ xx0-(diX_this),   yy0-(diY_this/2),  0] )  #7
        pt.append( [ xx0-(diX_this),   yy0+(diY_this/2),  0] )  #8
        crvX=rs.AddPolyline(pt)
        
    elif(req==7):
        crvX=rs.AddCircle(xpt,diX)
    else:
        pt.append([xx0-diX_this, yy0-diY_this,0])
        pt.append([xx0+diX_this,yy0-diY_this,0])
        pt.append([xx0+diX_this,yy0+diY_this,0])
        pt.append([xx0-diX_this,yy0+diY_this,0])
        pt.append([xx0-diX_this,yy0-diY_this,0])
        crvX=rs.AddPolyline(pt)
    ####    construct dummy crvX for Octagon)
    dummy_pt=[]
    dummy_pt.append([xx0-diX_this, yy0-diY_this,0])
    dummy_pt.append([xx0+diX_this,yy0-diY_this,0])
    dummy_pt.append([xx0+diX_this,yy0+diY_this,0])
    dummy_pt.append([xx0-diX_this,yy0+diY_this,0])
    dummy_pt.append([xx0-diX_this,yy0-diY_this,0])
    dummy_crvX0=rs.AddPolyline(dummy_pt)
    dummy_crvcen=rs.CurveAreaCentroid(dummy_crvX0)[0]
    dummy_crvX=rs.RotateObject(dummy_crvX0,dummy_crvcen,45,[0,0,1],False)

    if(req==1):
        diX2=diX_this*0.750
        diX3=diX_this*1.15
        diX4=diX_this*1.575
        crvX_off=rs.OffsetCurve(dummy_crvX,[pt[0][0]-10000,pt[0][1],0],diX2)  
        crvX_off1=rs.OffsetCurve(dummy_crvX,[pt[0][0]-10000,pt[0][1],0],diX3)
        crvX_off2=rs.OffsetCurve(dummy_crvX,[pt[0][0]-10000,pt[0][1],0],diX4)
    else:
        diX2=diX_this*0.650
        diX3=diX_this*0.950
        diX4=diX_this*1.325
        crvX_off=rs.OffsetCurve(crvX,[pt[0][0]-10000,pt[0][1],0],diX2)
        crvX_off1=rs.OffsetCurve(crvX,[pt[0][0]-10000,pt[0][1],0],diX3)
        crvX_off2=rs.OffsetCurve(crvX,[pt[0][0]-10000,pt[0][1],0],diX4)
    try:
        temp=[]
        for i in all_subdiv_crvs:
            c=rs.AddPolyline(i)
            m=rs.CurveCurveIntersection(c,crvX_off)
            if(m is not None):
                bx=rs.CurveBooleanDifference(c,crvX_off)
                bool_crvs.append(bx)
                temp.append(i)
            rs.DeleteObject(c)
        for i in temp:
            all_subdiv_crvs.remove(i)
        clear_list(temp)
        for i in all_subdiv_crvs:
            c=rs.AddPolyline(i)
            shapeCross(c)
            rs.DeleteObject(c)
    except:
        pass
    
    try:
        temp=[]
        for c in bool_crvs:
            if(rs.IsCurve(c)):
                m=rs.CurveCurveIntersection(c,crvX_off)
                if(m is not None):
                    bx=rs.CurveBooleanDifference(c,crvX_off)
                    temp.append(bx)
                    rs.DeleteObject(c)
        for i in temp:
            if( i not in bool_crvs):
                bool_crvs.append(i)
        for i in bool_crvs:
            if(rs.IsCurve(i)):
                shapeCross(i)
        clear_list(temp)
    except:
        pass
    
    ####    cut the border_curve with crvX_off1
    try:
        ar0=rs.CurveArea(site_crv)[0]
        temp1=[]
        k=0
        for i in new_all_border_crvs:
            ar1=rs.CurveArea(rs.coercecurve(i))[0]
            if(ar0/ar1 >16):#the smallest border
                m=rs.CurveCurveIntersection(rs.coercecurve(i),crvX_off1)
                if(m is not None):
                    bx=rs.CurveBooleanDifference(rs.coercecurve(i),crvX_off1)
                    temp1.append(i)
                    new_all_border_crvs.insert(k,bx)
                    new_all_border_crvs.remove(i)
            if(ar0/ar1 >4 and ar0/ar1 <8):#the smallest border
                m=rs.CurveCurveIntersection(rs.coercecurve(i),crvX_off2)
                if(m is not None):
                    bx=rs.CurveBooleanDifference(rs.coercecurve(i),crvX_off2)
                    temp1.append(i)
                    new_all_border_crvs.insert(k,bx)
                    new_all_border_crvs.remove(i)
            k+=1
    except:
        pass
    try:
        rs.DeleteObjects(temp1)
    except:
        pass
    ####    cut the first L-Border Curve with crvX_off1
    try:
        temp=[]
        for i in shaped_border_crvs[0]:
            temp.append(i)
        li=[]
        for i in temp:
            c=rs.AddPolyline(i)
            if(rs.IsCurve(c)):
                pt=rs.CurvePoints(c)[1]
                d1=rs.Distance(pt,crvcen)
                li.append([i,d1])
            rs.DeleteObject(c)
        lix=sorted(li,key=operator.itemgetter(1))
        temp2=[]
        clear_list(temp)
        for i in range(0,n,1):
            c=rs.AddPolyline(lix[i][0])
            m=rs.CurveCurveIntersection(c,crvX_off1)
            if(m is not None):
                cp=processLcurve(rs.CurvePoints(c))
                cx=rs.AddPolyline(cp)
                bx=rs.CurveBooleanDifference(cx,crvX_off1)
                rs.DeleteObject(cx)
                bool_crvs.append(bx)
                temp2.append(lix[i][0])
            rs.DeleteObject(c)
        clear_list(temp)
        k=0
        for i in temp2:
            if(i in shaped_border_crvs[0]):
                shaped_border_crvs[0].remove(i)
                k+1
    except:
        pass
    ####    cut the second L-Border Curve with crvX_off2
    try:
        temp=[]
        for i in shaped_border_crvs[0]:
            temp.append(i)
        li=[]
        for i in temp:
            c=rs.AddPolyline(i)
            if(rs.IsCurve(c)):
                pt=rs.CurvePoints(c)[1]
                d1=rs.Distance(pt,crvcen)
                li.append([i,d1])
            rs.DeleteObject(c)
        lix=sorted(li,key=operator.itemgetter(1))
        temp2=[]
        clear_list(temp)
        for i in range(0,n,1):
            c=rs.AddPolyline(lix[i][0])
            m=rs.CurveCurveIntersection(c,crvX_off2)
            if(m is not None):
                cp=processLcurve(rs.CurvePoints(c))
                cx=rs.AddPolyline(cp)
                bx=rs.CurveBooleanDifference(cx,crvX_off2)
                rs.DeleteObject(cx)
                bool_crvs.append(bx)
                temp2.append(lix[i][0])
            rs.DeleteObject(c)
        clear_list(temp)
        k=0
        for i in temp2:
            if(i in shaped_border_crvs[0]):
                shaped_border_crvs[0].remove(i)
                k+=1
    except:
        pass
    ####    delete the offset curves from the central canal
    try:
        rs.DeleteObjects([dummy_crvX,crvX_off,crvX_off1])
        pass
    except:
        pass
    try:
        rs.DeleteObject([crvX_off2])
        pass
    except:
        pass
    #####       this is the central canal
    #rs.EnableRedraw(True)
    return crvX

def initialize(crv, r0):
    rs.EnableRedraw(False)
    try:
        clear_list(new_crvs)
    except:
        pass
    try:
        rs.DeleteObjects(site_labels)
    except:
        pass
    r=float(r0)
    crv_pts=rs.CurvePoints(crv)
    x0=crv_pts[0][0]
    y0=crv_pts[0][1]
    x1=crv_pts[1][0]
    y1=crv_pts[1][1]
    x2=crv_pts[2][0]
    y2=crv_pts[2][1]
    x3=crv_pts[3][0]
    y3=crv_pts[3][1]
    
    li0=mid_pt(x0,y0,x1,y1)
    li1=mid_pt(x1,y1,x2,y2)
    li2=mid_pt(x2,y2,x3,y3)
    li3=mid_pt(x3,y3,x0,y0)
    
    site_labels.append(rs.AddTextDot("P",[x0,y0,0]))
    site_labels.append(rs.AddTextDot("P",[x1,y1,0]))
    site_labels.append(rs.AddTextDot("P",[x2,y2,0]))
    site_labels.append(rs.AddTextDot("P",[x3,y3,0]))
    site_labels.append(rs.AddTextDot("S",li0))
    site_labels.append(rs.AddTextDot("E",li1))
    site_labels.append(rs.AddTextDot("N",li2))
    site_labels.append(rs.AddTextDot("W",li3))
    
    nx0=li0[0]
    ny0=li0[1]
    nx1=li1[0]
    ny1=li1[1]
    nx2=li2[0]
    ny2=li2[1]
    nx3=li3[0]
    ny3=li3[1]
    
    # first curve
    crv1=rs.AddPolyline([[x0,y0,0],[nx0,ny0,0],[nx0,ny1,0],[nx3,ny3,0],[x0,y0,0]])
    mp1=mid_pt(x0,y0,nx0,ny1)
    crv1_f=rs.ScaleObject(crv1,mp1,[r,r,0])
    crv1_f_pts=rs.CurvePoints(crv1_f)
    rs.DeleteObject(crv1_f)
    rs.DeleteObject(crv1)
    # second curve
    crv2=rs.AddPolyline([[nx0,ny0,0],[x1,y1,0],[nx1,ny1,0],[nx0,ny1,0],[nx0,ny0,0]])
    mp2=mid_pt(nx0,ny0,nx1,ny1)
    crv2_f=rs.ScaleObject(crv2,mp2,[r,r,0])
    crv2_f_pts=rs.CurvePoints(crv2_f)
    rs.DeleteObject(crv2_f)
    rs.DeleteObject(crv2)
    # third curve
    crv3=rs.AddPolyline([[nx0,ny1,0],[nx1,ny1,0],[x2,y2,0],[nx2,ny2,0],[nx0,ny1,0]])
    mp3=mid_pt(nx0,ny1,x2,y2)
    crv3_f=rs.ScaleObject(crv3,mp3,[r,r,0])
    crv3_f_pts=rs.CurvePoints(crv3_f)
    rs.DeleteObject(crv3_f)
    rs.DeleteObject(crv3)
    # fourth curve
    crv4=rs.AddPolyline([[nx3,ny3,0],[nx0,ny1,0],[nx2,ny2,0],[x3,y3,0],[nx3,ny3,0]])
    mp4=mid_pt(nx3,ny3,nx2,ny2)
    crv4_f=rs.ScaleObject(crv4,mp4,[r,r,0])
    crv4_f_pts=rs.CurvePoints(crv4_f)
    rs.DeleteObject(crv4_f)
    rs.DeleteObject(crv4)
    
    p0=crv1_f_pts[0]
    p1=crv2_f_pts[1]
    p2=crv3_f_pts[2]
    p3=crv4_f_pts[3]
    can_1_bounding_crv.append([p0,p1,p2,p3,p0])
    
    new_crvs=[]
    new_crvs.append(crv1_f_pts)
    new_crvs.append(crv2_f_pts)
    new_crvs.append(crv3_f_pts)
    new_crvs.append(crv4_f_pts)
    rs.EnableRedraw(True)
    return new_crvs

def sub_div(new_crvs, gen, r):
    del_pt=[]
    for c in new_crvs:
        i=rs.AddPolyline(c)
        if(rs.IsCurve(i)):
            i_pt=rs.CurvePoints(i)
            for j in i_pt:
                y=rs.ScaleObject(i,j,[r/2,r/2,0], True)
                x=rs.CurvePoints(y)
                del_pt.append(x)
                rs.DeleteObject(y)
        rs.DeleteObject(i)
    return del_pt

def trimBorder(all_subdiv_crvs, all_border_crv_pts):
    L_border=[]
    line_border=[]
    for c1 in all_subdiv_crvs:
        crv1=rs.AddPolyline(c1)
        for c2 in all_border_crv_pts:
            crv2=rs.AddPolyline(c2)
            if(rs.IsCurve(crv1) and rs.IsCurve(crv2)):
                n=rs.CurveCurveIntersection(crv1,crv2)
                if(n is not None):
                    p1=n[0][1]
                    p2=n[1][1]
                    a=rs.Angle(p1,p2)[0]
                    if((a==0.0) or (a==-90.0) or (a>89 and a<91) or (a>179 and a<181) or (a>-181 and a<-179)):
                        line_border.append([p1,p2])
                    else:
                        crv2pt=rs.CurvePoints(crv2)
                        for pt in crv2pt:
                            m=rs.PointInPlanarClosedCurve(pt,crv1)
                            if(m==1):
                                L_border.append([p1,pt,p2])
            rs.DeleteObject(crv2)
        rs.DeleteObject(crv1)
    
    ####    start of full algo    #####
    xtemp_line_border=[]
    overlap_line_border=[]
    for i in line_border:
        crv1=rs.AddPolyline(i)
        sum=0
        for j in L_border:
            crv2=rs.AddPolyline(j)
            m=rs.CurveCurveIntersection(crv1,crv2)
            rs.DeleteObject(crv2)
            if(m is None):
                pass
            else:
                p1=rs.CurveStartPoint(crv1)
                p2=rs.CurveEndPoint(crv1)
                p3=m[0][1]
                d1=rs.Distance(p1,p3)
                d2=rs.Distance(p2,p3)
                if(d1>d2):
                    overlap_line_border.append([p1,p3])
                else:
                    overlap_line_border.append([p2,p3])
                sum+=1
        if(sum==0):
            xtemp_line_border.append(i)
        rs.DeleteObject(crv1)
    
    ####    eliminate overlapping line segments
    line_border=[]
    for i in overlap_line_border:
        if(i not in line_border):
            line_border.append(i)
    dup_line_border=line_border
    
    for i in line_border:
        d1=rs.Distance(i[0],i[1])
        for j in dup_line_border:
            d2=rs.Distance(j[0],j[1])
            if(i[0]==j[0] and d1<d2):
                dup_line_border.remove(j)
                break
    
    ####    plot / delete borders
    final_line_border=[]
    for i in xtemp_line_border:
        if(i not in final_line_border):
            final_line_border.append(i)
    
    for i in dup_line_border:
        if(i not in final_line_border):
            final_line_border.append(i)
    
    line_border_crvs=[]
    temp_line_border_crvs=[]
    for i in final_line_border:
        if(i not in temp_line_border_crvs):
            temp_line_border_crvs.append(i)
    for i in temp_line_border_crvs:
        #c=rs.AddPolyline(i)        #########################################################
        line_border_crvs.append(i)  #########################################################
    
    L_border_crvs=[]
    temp_L_border_crvs=[]
    for i in L_border:
        if(i not in temp_L_border_crvs):
                temp_L_border_crvs.append(i)
    for i in temp_L_border_crvs:
        #c=rs.AddPolyline(i)    #############################################################
        L_border_crvs.append(i) #############################################################
    
    border_crvs=[]
    border_crvs.append(L_border_crvs)
    border_crvs.append(line_border_crvs)
    
    ####    end of full algo    #####
    return border_crvs

def processLcurve(crvpt):
    #crvpt=rs.CurvePoints(crv)
    x0=crvpt[0][0]
    y0=crvpt[0][1]
    x1=crvpt[1][0]
    y1=crvpt[1][1]
    x2=crvpt[2][0]
    y2=crvpt[2][1]
    if((math.fabs(x1-x0)<0.001) and (math.fabs(y1==y2)<0.001)):
        x3=x2
        y3=y0
        pl=[[x0,y0,0],[x1,y1,0],[x2,y2,0],[x3,y3,0],[x0,y0,0]]
        #print("con 1")
    elif((math.fabs(x1-x2)<0.001) and (math.fabs(y1-y0)<0.001)):
        x3=x0
        y3=y2
        pl=[[x0,y0,0],[x1,y1,0],[x2,y2,0],[x3,y3,0],[x0,y0,0]]
        #print("con 2")
    else:
        x3=x2
        y3=y0
        pl=[[x0,y0,0],[x1,y1,0],[x2,y2,0],[x3,y3,0],[x0,y0,0]]
        #print("con 3")
    """
    rs.AddTextDot("0",[x0,y0,0])
    rs.AddTextDot("1",[x1,y1,0])
    rs.AddTextDot("2",[x2,y2,0])
    rs.AddTextDot("3",[x3,y3,0])
    """
    
    return pl

def main_canal_sys(crv0, canal_gen,diX,diY,idx, r):
    rs.EnableRedraw(False)
    try:
        clear_list(canal_pl_pts)
    except:
        pass
    try:
        rs.DeleteObjects(canal_pl)
    except:
        pass
    crv_pts=rs.CurvePoints(crv0)
    x0=crv_pts[0][0]
    y0=crv_pts[0][1]
    x1=crv_pts[1][0]
    y1=crv_pts[1][1]
    x2=crv_pts[2][0]
    y2=crv_pts[2][1]
    x3=crv_pts[3][0]
    y3=crv_pts[3][1]
    mx0=(x0+x1)/2
    my0=(y0+y1)/2
    mx1=(x1+x2)/2
    my1=(y1+y2)/2
    mx2=(x2+x3)/2
    my2=(y2+y3)/2
    mx3=(x3+x0)/2
    my3=(y3+y0)/2
    canal_arms.append(rs.AddLine([mx0,my0,0],[mx2,my2,0]))
    canal_arms.append(rs.AddLine([mx1,my1,0],[mx3,my3,0]))
    pt=rs.CurveAreaCentroid(crv0)[0]
    p1=rs.AddPoint(all_subdiv_crvs[0][0])
    p2=rs.AddPoint(all_subdiv_crvs[0][1])
    p3=rs.AddPoint(all_subdiv_crvs[0][2])
    diX0=rs.Distance(p1,p2)
    diY0=rs.Distance(p2,p3)
    rs.DeleteObject(p1)
    rs.DeleteObject(p2)
    rs.DeleteObject(p3)
    c0=rs.AddPolyline(all_subdiv_crvs[0])
    a=math.sqrt(rs.CurveArea(c0)[0])
    r0=(a/200)*can_arm_1.Value*2
    r1=(a/200)*can_arm_2.Value*2
    r2=(a/200)*can_arm_3.Value*2
    rs.DeleteObject(c0)
    if(idx<1):
        canal_pl=modulate(pt,4,r,r,1,diX0,diY0,0)
        canal_pl_pts=rs.CurvePoints(canal_pl)
        canal_cen=rs.CurveAreaCentroid(canal_pl)[0]
        canal_pl_offset.append(rs.OffsetCurve(canal_pl,canal_cen,r0))
    elif(idx>0 and idx<5):
        canal_pl=modulate(pt,4,r,r,2,diX0,diY0,0)
        canal_pl_pts=rs.CurvePoints(canal_pl)
        canal_cen=rs.CurveAreaCentroid(canal_pl)[0]
        canal_pl_offset.append(rs.OffsetCurve(canal_pl,canal_cen,r1))
    else:
        canal_pl=modulate(pt,4,r,r,2,diX0,diY0,2)# to interact with booleasn curves
        canal_pl_pts=rs.CurvePoints(canal_pl)
        canal_cen=rs.CurveAreaCentroid(canal_pl)[0]
        canal_pl_offset.append(rs.OffsetCurve(canal_pl,canal_cen,r2))
    rs.EnableRedraw(True)
    return canal_pl

def draw_canal_arms_init(sender, e):
    rs.EnableRedraw(False)
    try:
        rs.DeleteObjects(stage1_dummy_canal_arms)
    except:
        pass    
    try:
        rs.DeleteObjects(dummy_canal_arms)
        clear_list(dummy_canal_arms)
    except:
        pass
    try:
        clear_list(canal_cen_pts)
    except:
        pass
    #dummy_canal_arm_pts=[]
    try:
        clear_list(dummy_canal_arm_pts)
    except:
        pass
    try:
        rs.DeleteObjects(temp_del_canal_arms)
    except:
        pass
    try:
        rs.DeleteObjects(canal_arm_gen_pts)
        clear_list(canal_arm_gen_pts)
    except:
        pass
    
    try:
        rs.DeleteObjects(canal_arrows)
    except:
        pass
    try:
        rs.DeleteObjects(stage1_dummy_canal_arms)
    except:
        pass
    
    #r0=(ar/200)*can_arm_1.Value
    #r1=(ar/200)*can_arm_2.Value
    #r2=(ar/200)*can_arm_3.Value
    ar=math.sqrt(rs.CurveArea(site_crv)[0])/12
    if(can_1_yes.Checked==True):
        r0=(ar/200)*can_arm_1.Value/2
        for i in can_1_bounding_crv:
            crv_pts=i
            x0=crv_pts[0][0]
            y0=crv_pts[0][1]
            x1=crv_pts[1][0]
            y1=crv_pts[1][1]
            x2=crv_pts[2][0]
            y2=crv_pts[2][1]
            x3=crv_pts[3][0]
            y3=crv_pts[3][1]
            mx0=(x0+x1)/2
            my0=(y0+y1)/2
            mx1=(x1+x2)/2
            my1=(y1+y2)/2
            mx2=(x2+x3)/2
            my2=(y2+y3)/2
            mx3=(x3+x0)/2
            my3=(y3+y0)/2
            ver=rs.AddLine([mx0,my0,0],[mx2,my2,0])
            hor=rs.AddLine([mx1,my1,0],[mx3,my3,0])
            canal_arm_gen_pts.append([mx0,my0,0])
            canal_arm_gen_pts.append([mx2,my2,0])
            canal_arm_gen_pts.append([mx1,my1,0])
            canal_arm_gen_pts.append([mx3,my3,0])
            sp=rs.CurveMidPoint(ver)
            #canal_cen_pts.append(sp)
            l1=(rs.OffsetCurve(ver,[sp[0]-10,sp[1],0],r0))
            l2=(rs.OffsetCurve(ver,[sp[0]+10,sp[1],0],r0))
            pl1=rs.AddPolyline([rs.CurveEndPoint(l1),rs.CurveStartPoint(l1),rs.CurveStartPoint(l2),rs.CurveEndPoint(l2),rs.CurveEndPoint(l1)])
            rs.DeleteObjects([l1,l2])
            l3=(rs.OffsetCurve(hor,[sp[0],sp[1]-10,0],r0))
            l4=(rs.OffsetCurve(hor,[sp[0],sp[1]+10,0],r0))
            pl2=rs.AddPolyline([rs.CurveEndPoint(l3),rs.CurveStartPoint(l3),rs.CurveStartPoint(l4),rs.CurveEndPoint(l4),rs.CurveEndPoint(l3)])
            rs.DeleteObjects([l3,l4,ver,hor])
            bool_un=rs.CurveBooleanUnion([pl1,pl2])
            bool_un_pts=rs.CurvePoints(bool_un)
            dummy_canal_arm_pts.append(bool_un_pts)
            rs.DeleteObjects([pl1,pl2])
            rs.DeleteObject(bool_un)
        try:
            clear_list(canal_cen_pts)
        except:
            pass
        for i in all_border_crv_pts:
            c=rs.AddPolyline(i)
            p=rs.CurveAreaCentroid(c)[0]
            canal_cen_pts.append(p)
            rs.DeleteObject(c)
            
    if(can_2_yes.Checked==True):
        r1=(ar/200)*can_arm_2.Value/2
        for i in crv_gen_1:
            crv_pts=i
            x0=crv_pts[0][0]
            y0=crv_pts[0][1]
            x1=crv_pts[1][0]
            y1=crv_pts[1][1]
            x2=crv_pts[2][0]
            y2=crv_pts[2][1]
            x3=crv_pts[3][0]
            y3=crv_pts[3][1]
            mx0=(x0+x1)/2
            my0=(y0+y1)/2
            mx1=(x1+x2)/2
            my1=(y1+y2)/2
            mx2=(x2+x3)/2
            my2=(y2+y3)/2
            mx3=(x3+x0)/2
            my3=(y3+y0)/2
            ver=rs.AddLine([mx0,my0,0],[mx2,my2,0])
            hor=rs.AddLine([mx1,my1,0],[mx3,my3,0])
            canal_arm_gen_pts.append([mx0,my0,0])
            canal_arm_gen_pts.append([mx2,my2,0])
            canal_arm_gen_pts.append([mx1,my1,0])
            canal_arm_gen_pts.append([mx3,my3,0])
            sp=rs.CurveMidPoint(ver)
            #canal_cen_pts.append(sp)
            l1=(rs.OffsetCurve(ver,[sp[0]-10,sp[1],0],r1))
            l2=(rs.OffsetCurve(ver,[sp[0]+10,sp[1],0],r1))
            pl1=rs.AddPolyline([rs.CurveEndPoint(l1),rs.CurveStartPoint(l1),rs.CurveStartPoint(l2),rs.CurveEndPoint(l2),rs.CurveEndPoint(l1)])
            rs.DeleteObjects([l1,l2])
            l3=(rs.OffsetCurve(hor,[sp[0],sp[1]-10,0],r1))
            l4=(rs.OffsetCurve(hor,[sp[0],sp[1]+10,0],r1))
            pl2=rs.AddPolyline([rs.CurveEndPoint(l3),rs.CurveStartPoint(l3),rs.CurveStartPoint(l4),rs.CurveEndPoint(l4),rs.CurveEndPoint(l3)])
            rs.DeleteObjects([l3,l4,ver,hor])
            bool_un=rs.CurveBooleanUnion([pl1,pl2])
            bool_un_pts=rs.CurvePoints(bool_un)
            dummy_canal_arm_pts.append(bool_un_pts)
            rs.DeleteObjects([pl1,pl2])
            rs.DeleteObject(bool_un)

    if(can_3_yes.Checked==True):
        r2=(ar/200)*can_arm_3.Value/2
        for i in crv_gen_2:
            crv_pts=i
            x0=crv_pts[0][0]
            y0=crv_pts[0][1]
            x1=crv_pts[1][0]
            y1=crv_pts[1][1]
            x2=crv_pts[2][0]
            y2=crv_pts[2][1]
            x3=crv_pts[3][0]
            y3=crv_pts[3][1]
            mx0=(x0+x1)/2
            my0=(y0+y1)/2
            mx1=(x1+x2)/2
            my1=(y1+y2)/2
            mx2=(x2+x3)/2
            my2=(y2+y3)/2
            mx3=(x3+x0)/2
            my3=(y3+y0)/2
            ver=rs.AddLine([mx0,my0 ,0],[mx2,my2 ,0])
            hor=rs.AddLine([mx1 ,my1,0],[mx3 ,my3,0])
            #canal_arm_gen_pts.append([mx0,my0,0])
            #canal_arm_gen_pts.append([mx2,my2,0])
            #canal_arm_gen_pts.append([mx1,my1,0])
            #canal_arm_gen_pts.append([mx3,my3,0])
            sp=rs.CurveMidPoint(ver)
            #canal_cen_pts.append(sp)
            l1=(rs.OffsetCurve(ver,[sp[0]-10,sp[1],0],r2))
            l2=(rs.OffsetCurve(ver,[sp[0]+10,sp[1],0],r2))
            pl1=rs.AddPolyline([rs.CurveEndPoint(l1),rs.CurveStartPoint(l1),rs.CurveStartPoint(l2),rs.CurveEndPoint(l2),rs.CurveEndPoint(l1)])
            rs.DeleteObjects([l1,l2])
            l3=(rs.OffsetCurve(hor,[sp[0],sp[1]-10,0],r2))
            l4=(rs.OffsetCurve(hor,[sp[0],sp[1]+10,0],r2))
            pl2=rs.AddPolyline([rs.CurveEndPoint(l3),rs.CurveStartPoint(l3),rs.CurveStartPoint(l4),rs.CurveEndPoint(l4),rs.CurveEndPoint(l3)])
            rs.DeleteObjects([l3,l4,ver,hor])
            bool_un=rs.CurveBooleanUnion([pl1,pl2])
            bool_un_pts=rs.CurvePoints(bool_un)
            dummy_canal_arm_pts.append(bool_un_pts)
            rs.DeleteObjects([pl1,pl2])
            rs.DeleteObject(bool_un)
    #print(can_arm_1.Value)
    #print(can_arm_2.Value)
    #print(can_arm_3.Value)
    for i in dummy_canal_arm_pts:
        dummy_canal_arms.append(rs.AddPolyline(i))
    rs.EnableRedraw(True)

def draw_reservoir_init(sender,e):
    rs.EnableRedraw(False)
    try:
        rs.DeleteObjects(shape_cross)
    except:
        pass
    try:
        rs.DeleteObjects(stage1_dummy_canal_arms)
    except:
        pass    
    try:
        rs.DeleteObjects(def_canal_arms)
        #clear_list(def_canal_arms)
    except:
        pass
    
    try:
        rs.DeleteObjects(canal_pl)
        #clear_list(canal_pl)
    except:
        pass
    
    try:
        clear_list(canal_pl_pts)
    except:
        pass
    
    try:
        rs.DeleteObjects(temp_del_list_subdiv)
    except:
        pass
    try:
        rs.DeleteObjects(temp_del_list_border)
    except:
        pass
    try:
        clear_list(def0_canal_arm)
        #rs.DeleteObjects(def0_canal_arm)
    except:
        pass
    try:
        rs.DeleteObjects(tmp0_indent)
        clear_list(tmp0_indent)
    except:
        pass
    #dummy_canal_arms=[]
    try:
        rs.DeleteObjects(dummy_canal_arms)
        clear_list(dummy_canal_arms)
    except:
        pass
    #dummy_canal_pl_pts=[]
    try:
        clear_list(dummy_canal_pl_pts)
    except:
        pass
    #dummy_canal_pl_crvs=[]
    try:
        rs.DeleteObjects(dummy_canal_pl_crvs)
        clear_list(dummy_canal_pl_crvs)
    except:
        pass
    try:
        clear_list(canal_cen_pts)
    except:
        pass
    #dummy_res_pts=[]
    try:
        clear_list(dummy_res_pts)
    except:
        pass
    try:
        rs.DeleteObjects(final_canal_sys)
    except:
        pass
    try:
        rs.DeleteObjects(new_shaped_border_crvs_res_1)
    except:
        pass
    try:
        rs.DeleteObjects(new_shaped_border_crvs_res_1)
    except:
        pass
    try:
        rs.DeleteObjects(new_shaped_border_crvs_res_2)
    except:
        pass
    canal_bnd_crvs=[]
    canal_bnd_crvs.append(can_1_bounding_crv[0])
    
    for i in crv_gen_1:
        canal_bnd_crvs.append(i)
    for i in crv_gen_2:
        canal_bnd_crvs.append(i)
    
    
    c0=rs.CopyObject(site_crv,[0,0,0])
    c0pt=rs.CurvePoints(c0)
    diX=rs.Distance(c0pt[0],c0pt[1])/12
    diY=rs.Distance(c0pt[1],c0pt[2])/12
    ar=math.sqrt(rs.CurveArea(c0)[0])/20
    """
    if(can_arm_1.Value>1.5):
        r0=(ar/200)*can_arm_1.Value
    else:
        r0=(ar/200)*20
    if(can_arm_2.Value>1.5):
        r1=(ar/200)*can_arm_2.Value
    else:
        r1=(ar/200)*15
    if(can_arm_3.Value>1.5):
        r2=(ar/200)*can_arm_3.Value
    else:
        r2=(ar/200)*10
        """
    r0=(subdiv_ratio1.Value)/500
    r1=(ui_border_ratio.Value/1000)**2*r0
    r2=(ui_border_ratio.Value/1000)**2*r1*0.85
    rs.DeleteObject(c0)    
    #print(str(r0)+";"+str(r1)+";"+str(r2))
    #res_ratio
    m=1.0
    n=1.0
    p=1.0
    k=0
    site_area=rs.CurveArea(site_crv)[0]
    for i in canal_bnd_crvs:
        c=rs.AddPolyline(i)
        c_ar=rs.CurveArea(c)[0]
        #print(str(k)+","+str(int(site_area/c_ar)))
        p=rs.CurveAreaCentroid(c)[0]
        if(p not in canal_cen_pts):
            canal_cen_pts.append(p)
            #central canal system
            if(c_ar>site_area/2):
                geo1=100
                if(can_1_oct.Checked==True and can_1_sq.Checked==False and can_1_yes.Checked==True):
                    geo1=1
                elif(can_1_oct.Checked==False and can_1_sq.Checked==True and can_1_yes.Checked==True):
                    geo1=2
                else:
                    geo1=100
                if(geo1==1 or geo1==2):
                    dummy_canal_pl_crvs.append(modulate(p,4,r0,r0,geo1,diX,diY,0))
            #first gen canal system
            elif(c_ar>site_area/8 and c_ar<=site_area/4):
                geo2=100
                if(can_2_oct.Checked==True and can_2_sq.Checked==False and can_2_yes.Checked==True):
                    geo2=1
                elif(can_2_oct.Checked==False and can_2_sq.Checked==True and can_2_yes.Checked==True):
                    geo2=2
                else:
                    geo2=100
                if(geo2==1 or geo2==2):
                    dummy_canal_pl_crvs.append(modulate(p,4,r1,r1,geo2,diX,diY,2))
            #second gen canal system
            else:
                geo3=100
                if(can_3_oct.Checked==True and can_3_sq.Checked==False and can_3_yes.Checked==True):
                    geo3=1
                elif(can_3_sq.Checked==True and can_3_oct.Checked==False and can_3_yes.Checked==True):
                    geo3=2
                else:
                    geo3=100
                if(geo3==1 or geo3==2):
                   dummy_canal_pl_crvs.append(modulate(p,4,r2,r2,geo3,diX,diY,2))
        rs.DeleteObject(c)
        k+=1
    
    for i in dummy_canal_pl_crvs:
        dummy_canal_pl_pts.append(rs.CurvePoints(i))
    
    for i in dummy_canal_arm_pts:
        c=rs.AddPolyline(i)
        for j in dummy_canal_pl_crvs:
            try:
                inx=rs.CurveCurveIntersection(c,j)
                if(inx is not None):
                    y=rs.CurveBooleanUnion([j,c])
                    if(rs.IsCurve(y)):
                        final_canal_sys.append(y)
                    else:
                        rs.DeleteObject(y)
                    rs.DeleteObject(c)
                    break
            except:
                pass
    k=0
    
    rs.DeleteObjects(dummy_canal_pl_crvs)
    rs.DeleteObjects(dummy_canal_arms)
    
    ###PLOT ALL CURVES
    for i in all_subdiv_crvs:
        temp_del_list_subdiv.append(rs.AddPolyline(i))
    try:
        for i in shaped_border_crvs[0]:
            temp_del_list_border.append(rs.AddPolyline([i]))
        for i in shaped_border_crvs[0]:
            temp_del_list_L_border.append(rs.AddPolyline(i))
        for i in shaped_border_crvs[1]:
            temp_del_list_line_border.append(rs.AddPolyline(i))
    except:
        pass
    ###CONSTRUCT RESERVOIR OFFSET
    for i in dummy_canal_pl_pts:
            if(k==0):
                if(can_arm_1.Value<1.5):
                    dummy_canal_pl_crvs.append(rs.AddPolyline(i))
                else:
                    pass
                c=rs.AddPolyline(i)
                dummy_res_pts.append(rs.CurvePoints(c))
                cc=rs.CurveAreaCentroid(c)[0]
                dummy_canal_pl_off_crvs.append(rs.OffsetCurve(c,cc,2*r0))
                rs.DeleteObject(c)
            elif(k>0 and k<5):
                if(can_arm_2.Value<1.5):
                    dummy_canal_pl_crvs.append(rs.AddPolyline(i))
                else:
                    pass
                c=rs.AddPolyline(i)
                dummy_res_pts.append(rs.CurvePoints(c))
                cc=rs.CurveAreaCentroid(c)[0]
                dummy_canal_pl_off_crvs.append(rs.OffsetCurve(c,cc,2*r1))
                rs.DeleteObject(c)
            else:
                if(can_arm_3.Value<1.5):
                    dummy_canal_pl_crvs.append(rs.AddPolyline(i))
                else:
                    pass
                c=rs.AddPolyline(i)
                dummy_res_pts.append(rs.CurvePoints(c))
                cc=rs.CurveAreaCentroid(c)[0]
                dummy_canal_pl_off_crvs.append(rs.OffsetCurve(c,cc,2*r2))
                rs.DeleteObject(c)
            k+=1
    rs.EnableRedraw(True)

def plot_canal_arms(diX,diY,diX0,diY0):
    rs.EnableRedraw(False)
    r=20
    def_canal_arm=[]
    try:
        rs.DeleteObjects(stage1_dummy_canal_arms)
    except:
        pass
    """
    try:
        rs.DeleteObjects(def_canal_arm)
        clear_list(def_canal_arm)
    except:
        pass
    """
    c0=rs.AddPolyline(all_subdiv_crvs[0])
    ar=math.sqrt(rs.CurveArea(c0)[0])
    r0=(ar/200)*can_arm_1.Value
    r1=(ar/200)*can_arm_2.Value
    r2=(ar/200)*can_arm_3.Value
    rs.DeleteObject(c0)
    for i in canal_arms:
        sp=rs.CurveStartPoint(i)
        ep=rs.CurveEndPoint(i)
        mp=rs.CurveMidPoint(i)
        indexes=canal_arms.index(i)
        if(indexes==0):
            del1=modulate(sp,2,1,1,0,diX0,diY0,0)
            rs.DeleteObject(del1)
            del2=modulate(ep,2,1,1,0,diX0,diY0,0)
            rs.DeleteObject(del2)
            a=rs.Angle(sp,mp)[0]
            if(a==90):
                if(sp[1]<mp[1]):
                    spx=[sp[0],sp[1]+ar/2,0]
                    mpx=[mp[0],mp[1],0]
                    l=rs.AddLine(spx,mpx)
                    l1=rs.OffsetCurve(l,[sp[0]-10,sp[1],0],r0)
                    l2=rs.OffsetCurve(l,[sp[0]+10,sp[1],0],r0)
                    plx=rs.AddPolyline([rs.CurveEndPoint(l1),rs.CurveStartPoint(l1),rs.CurveStartPoint(l2),rs.CurveEndPoint(l2),rs.CurveEndPoint(l1)])
                    for u in canal_pl:
                        m=rs.CurveCurveIntersection(plx,u)
                        if(m is not None):
                            crvCuX=rs.CurveBooleanDifference(plx,u)
                            def_canal_arm.append(rs.CurvePoints(crvCuX))
                            rs.DeleteObject(crvCuX)
                    rs.DeleteObject(plx)
                    rs.DeleteObject(l)
                    rs.DeleteObject(l1)
                    rs.DeleteObject(l2)
                if(ep[1]>mp[1]):
                    epx=[ep[0],ep[1]-ar/2,0]
                    mpx=[mp[0],mp[1],0]
                    l=rs.AddLine(epx,mpx)
                    l1=rs.OffsetCurve(l,[ep[0]-10,ep[1],0],r0)
                    l2=rs.OffsetCurve(l,[ep[0]+10,ep[1],0],r0)
                    plx=rs.AddPolyline([rs.CurveEndPoint(l1),rs.CurveStartPoint(l1),rs.CurveStartPoint(l2),rs.CurveEndPoint(l2),rs.CurveEndPoint(l1)])
                    for u in canal_pl:
                        m=rs.CurveCurveIntersection(plx,u)
                        if(m is not None):
                            crvCuX=rs.CurveBooleanDifference(plx,u)
                            def_canal_arm.append(rs.CurvePoints(crvCuX))
                            rs.DeleteObject(crvCuX)
                    rs.DeleteObject(plx)
                    rs.DeleteObject(l)
                    rs.DeleteObject(l1)
                    rs.DeleteObject(l2)                    
        if(indexes==1):
            del1=modulate(sp,2,1,1,0,diX0,diY0,0)
            rs.DeleteObject(del1)
            del2=modulate(ep,2,1,1,0,diX0,diY0,0)
            rs.DeleteObject(del2)
            a=rs.Angle(sp,mp)[0]
            if(a==180 or a==-180 or a==0):
                if(sp[0]>mp[0]):
                    spx=[sp[0]-ar/2,sp[1],0]
                    mpx=[mp[0],mp[1],0]
                    l=rs.AddLine(spx,mpx)
                    l1=rs.OffsetCurve(l,[sp[0],sp[1]-10,0],r0)
                    l2=rs.OffsetCurve(l,[sp[0],sp[1]+10,0],r0)
                    l3=rs.AddLine(rs.CurveStartPoint(l1),rs.CurveStartPoint(l2))
                    plx=rs.AddPolyline([rs.CurveEndPoint(l1),rs.CurveStartPoint(l1),rs.CurveStartPoint(l2),rs.CurveEndPoint(l2),rs.CurveEndPoint(l1)])
                    for u in canal_pl:
                        m=rs.CurveCurveIntersection(plx,u)
                        if(m is not None):
                            crvCuX=rs.CurveBooleanDifference(plx,u)
                            def_canal_arm.append(rs.CurvePoints(crvCuX))
                            rs.DeleteObject(crvCuX)
                    rs.DeleteObject(plx)
                    rs.DeleteObject(l)
                    rs.DeleteObject(l1)
                    rs.DeleteObject(l2)
                    rs.DeleteObject(l3)
                if(ep[0]<mp[0]):
                    epx=[ep[0]+ar/2,ep[1],0]
                    mpx=[mp[0],mp[1],0]
                    l=rs.AddLine(epx,mpx)
                    l1=rs.OffsetCurve(l,[ep[0],ep[1]-10,0],r0)
                    l2=rs.OffsetCurve(l,[ep[0],ep[1]+10,0],r0)
                    l3=rs.AddLine(rs.CurveStartPoint(l1),rs.CurveStartPoint(l2))
                    plx=rs.AddPolyline([rs.CurveEndPoint(l1),rs.CurveStartPoint(l1),rs.CurveStartPoint(l2),rs.CurveEndPoint(l2),rs.CurveEndPoint(l1)])
                    for u in canal_pl:
                        m=rs.CurveCurveIntersection(plx,u)
                        if(m is not None):
                            crvCuX=rs.CurveBooleanDifference(plx,u)
                            def_canal_arm.append(rs.CurvePoints(crvCuX))
                            rs.DeleteObject(crvCuX)
                    rs.DeleteObject(plx)
                    rs.DeleteObject(l)
                    rs.DeleteObject(l1)
                    rs.DeleteObject(l2)                    
                    rs.DeleteObject(l3)
        elif(indexes>1 and indexes<5):
            a=rs.Angle(sp,mp)[0]
            if(a==90 or a==-90):
                if(sp[1]<mp[1]):
                    spx=[sp[0],sp[1],0]
                    mpx=[mp[0],mp[1],0]
                    l=rs.AddLine(spx,mpx)
                    l1=rs.OffsetCurve(l,[sp[0]-10,sp[1],0],r1)
                    l2=rs.OffsetCurve(l,[sp[0]+10,sp[1],0],r1)
                    plx=rs.AddPolyline([rs.CurveEndPoint(l1),rs.CurveStartPoint(l1),rs.CurveStartPoint(l2),rs.CurveEndPoint(l2),rs.CurveEndPoint(l1)])
                    for u in canal_pl:
                        m=rs.CurveCurveIntersection(plx,u)
                        if(m is not None):
                            crvCuX=rs.CurveBooleanDifference(plx,u)
                            def_canal_arm.append(rs.CurvePoints(crvCuX))
                            rs.DeleteObject(crvCuX)
                    rs.DeleteObject(plx)
                    rs.DeleteObject(l)
                    rs.DeleteObject(l1)
                    rs.DeleteObject(l2)
                if(ep[1]>mp[1]):
                    epx=[ep[0],ep[1],0]
                    mpx=[mp[0],mp[1],0]
                    l=rs.AddLine(epx,mpx)
                    l1=rs.OffsetCurve(l,[ep[0]-10,ep[1],0],r1)
                    l2=rs.OffsetCurve(l,[ep[0]+10,ep[1],0],r1)
                    plx=rs.AddPolyline([rs.CurveEndPoint(l1),rs.CurveStartPoint(l1),rs.CurveStartPoint(l2),rs.CurveEndPoint(l2),rs.CurveEndPoint(l1)])
                    for u in canal_pl:
                        m=rs.CurveCurveIntersection(plx,u)
                        if(m is not None):
                            crvCuX=rs.CurveBooleanDifference(plx,u)
                            def_canal_arm.append(rs.CurvePoints(crvCuX))
                            rs.DeleteObject(crvCuX)
                    rs.DeleteObject(plx)
                    rs.DeleteObject(l)
                    rs.DeleteObject(l1)
                    rs.DeleteObject(l2)
            if(a==180 or a==-180 or a==0):
                if(sp[0]>mp[0]):
                    spx=[sp[0],sp[1],0]
                    mpx=[mp[0],mp[1],0]
                    l=rs.AddLine(spx,mpx)
                    l1=rs.OffsetCurve(l,[sp[0],sp[1]-10,0],r1)
                    l2=rs.OffsetCurve(l,[sp[0],sp[1]+10,0],r1)
                    plx=rs.AddPolyline([rs.CurveEndPoint(l1),rs.CurveStartPoint(l1),rs.CurveStartPoint(l2),rs.CurveEndPoint(l2),rs.CurveEndPoint(l1)])
                    for u in canal_pl:
                        m=rs.CurveCurveIntersection(plx,u)
                        if(m is not None):
                            crvCuX=rs.CurveBooleanDifference(plx,u)
                            def_canal_arm.append(rs.CurvePoints(crvCuX))
                            rs.DeleteObject(crvCuX)
                    rs.DeleteObject(plx)
                    rs.DeleteObject(l)
                    rs.DeleteObject(l1)
                    rs.DeleteObject(l2)
                if(ep[0]<mp[0]):
                    epx=[ep[0],ep[1],0]
                    mpx=[mp[0],mp[1],0]
                    l=rs.AddLine(epx,mpx)
                    l1=rs.OffsetCurve(l,[ep[0],ep[1]-10,0],r1)
                    l2=rs.OffsetCurve(l,[ep[0],ep[1]+10,0],r1)
                    plx=rs.AddPolyline([rs.CurveEndPoint(l1),rs.CurveStartPoint(l1),rs.CurveStartPoint(l2),rs.CurveEndPoint(l2),rs.CurveEndPoint(l1)])
                    for u in canal_pl:
                        m=rs.CurveCurveIntersection(plx,u)
                        if(m is not None):
                            crvCuX=rs.CurveBooleanDifference(plx,u)
                            def_canal_arm.append(rs.CurvePoints(crvCuX))
                            rs.DeleteObject(crvCuX)
                    rs.DeleteObject(plx)
                    rs.DeleteObject(l)
                    rs.DeleteObject(l1) 
                    rs.DeleteObject(l2)
        elif(indexes>4):
            a=rs.Angle(sp,mp)[0]
            if(a==90 or a==-90):
                if(sp[1]<mp[1]):
                    spx=[sp[0],sp[1],0]
                    mpx=[mp[0],mp[1],0]
                    l=rs.AddLine(spx,mpx)
                    l1=rs.OffsetCurve(l,[sp[0]-10,sp[1],0],r2)
                    l2=rs.OffsetCurve(l,[sp[0]+10,sp[1],0],r2)
                    plx=rs.AddPolyline([rs.CurveEndPoint(l1),rs.CurveStartPoint(l1),rs.CurveStartPoint(l2),rs.CurveEndPoint(l2),rs.CurveEndPoint(l1)])
                    for u in canal_pl:
                        m=rs.CurveCurveIntersection(plx,u)
                        if(m is not None):
                            crvCuX=rs.CurveBooleanDifference(plx,u)
                            def_canal_arm.append(rs.CurvePoints(crvCuX))
                            rs.DeleteObject(crvCuX)
                    rs.DeleteObject(plx)
                    rs.DeleteObject(l)
                    rs.DeleteObject(l1)
                    rs.DeleteObject(l2)
                if(ep[1]>mp[1]):
                    epx=[ep[0],ep[1],0]
                    mpx=[mp[0],mp[1],0]
                    l=rs.AddLine(epx,mpx)
                    l1=rs.OffsetCurve(l,[ep[0]-10,ep[1],0],r2)
                    l2=rs.OffsetCurve(l,[ep[0]+10,ep[1],0],r2)
                    plx=rs.AddPolyline([rs.CurveEndPoint(l1),rs.CurveStartPoint(l1),rs.CurveStartPoint(l2),rs.CurveEndPoint(l2),rs.CurveEndPoint(l1)])
                    for u in canal_pl:
                        m=rs.CurveCurveIntersection(plx,u)
                        if(m is not None):
                            crvCuX=rs.CurveBooleanDifference(plx,u)
                            def_canal_arm.append(rs.CurvePoints(crvCuX))
                            rs.DeleteObject(crvCuX)
                    rs.DeleteObject(plx)
                    rs.DeleteObject(l)
                    rs.DeleteObject(l1)
                    rs.DeleteObject(l2)
            if(a==180 or a==-180 or a==0):
                if(sp[0]>mp[0]):
                    spx=[sp[0],sp[1],0]
                    mpx=[mp[0],mp[1],0]
                    l=rs.AddLine(spx,mpx)
                    l1=rs.OffsetCurve(l,[sp[0],sp[1]-10,0],r2)
                    l2=rs.OffsetCurve(l,[sp[0],sp[1]+10,0],r2)
                    plx=rs.AddPolyline([rs.CurveEndPoint(l1),rs.CurveStartPoint(l1),rs.CurveStartPoint(l2),rs.CurveEndPoint(l2),rs.CurveEndPoint(l1)])
                    for u in canal_pl:
                        m=rs.CurveCurveIntersection(plx,u)
                        if(m is not None):
                            crvCuX=rs.CurveBooleanDifference(plx,u)
                            def_canal_arm.append(rs.CurvePoints(crvCuX))
                            rs.DeleteObject(crvCuX)
                    rs.DeleteObject(plx)
                    rs.DeleteObject(l)
                    rs.DeleteObject(l1)
                    rs.DeleteObject(l2)
                if(ep[0]<mp[0]):
                    epx=[ep[0],ep[1],0]
                    mpx=[mp[0],mp[1],0]
                    l=rs.AddLine(epx,mpx)
                    l1=rs.OffsetCurve(l,[ep[0],ep[1]-10,0],r2)
                    l2=rs.OffsetCurve(l,[ep[0],ep[1]+10,0],r2)
                    plx=rs.AddPolyline([rs.CurveEndPoint(l1),rs.CurveStartPoint(l1),rs.CurveStartPoint(l2),rs.CurveEndPoint(l2),rs.CurveEndPoint(l1)])
                    for u in canal_pl:
                        m=rs.CurveCurveIntersection(plx,u)
                        if(m is not None):
                            crvCuX=rs.CurveBooleanDifference(plx,u)
                            def_canal_arm.append(rs.CurvePoints(crvCuX))
                            rs.DeleteObject(crvCuX)
                    rs.DeleteObject(plx)
                    rs.DeleteObject(l)
                    rs.DeleteObject(l1) 
                    rs.DeleteObject(l2)
    rs.EnableRedraw(True)
    return def_canal_arm

def draw_initialize(sender,e):
    #temp_del_list_gen_ini_crvs=[]
    try:
        rs.DeleteObjects(temp_del_list_gen_ini_crvs)
    except:
        pass
    #gen_crvs_ini=[]
    try:
        clear_list(gen_crvs_ini)
    except:
        pass
    
    #gen_crvs=[]
    try:
        clear_list(gen_crvs)
    except:
        pass
    
    #gen_crvs_0
    try:
        clear_list(crv_gen_0)
    except:
        pass

    #gen_crvs_1
    try:
        clear_list(crv_gen_1)
    except:
        pass
    try:
        rs.DeleteObjects(new_all_border_crvs)
    except:
        pass
    try:
        clear_list(new_all_border_crvs)
    except:
        pass
    try:
        rs.DeleteObjects(new_shaped_border_crvs_res_1)
    except:
        pass
    try:
        rs.DeleteObjects(new_shaped_border_crvs_res_2)
    except:
        pass
    try:
        rs.DeleteObjects(new_shaped_border_crvs_res_3)
    except:
        pass
    try:
        rs.DeleteObjects(site_labels)
    except:
        pass
    r0=subdiv_ratio1.Value/1000
    crv_gen_0.append(rs.CurvePoints(site_crv))
    gen_crvs.append(rs.CurvePoints(site_crv))    
    crv0=[]
    crv0=initialize(site_crv, r0)
    for i in crv0:
        if(i not in gen_crvs_ini):
            crv_gen_1.append(i)
            gen_crvs_ini.append(i)
            gen_crvs.append(i)
            temp_del_list_gen_ini_crvs.append(rs.AddPolyline(i))

def draw_subdiv(sender, e):
    rs.EnableRedraw(False)    
    try:
        rs.DeleteObjects(shape_cross)
    except:
        pass
    #temp_del_list_subdiv=[]
    try:
        rs.DeleteObjects(temp_del_list_subdiv)
    except:
        pass
        
    #temp_del_list_gen=[]
    try:
        rs.DeleteObjects(temp_del_list_gen)
    except:
        pass
    
    #temp_del_list_gen_crvs=[]
    try:
        rs.DeleteObjects(temp_del_list_gen_crvs)
    except:
        pass
    
    #all_subdiv_crvs=[]
    try:
        clear_list(all_subdiv_crvs)
    except:
        pass
    
    #gen_crvs=[]
    try:
        clear_list(gen_crvs)
    except:
        pass        
    try:
        temp_del_list_gen_crvs
    except:
        pass
        
    #n_crv=[]
    try:
        clear_list(n_crv)
    except:
        pass
    try:
        if(gen_crvs_ini is not None):
            for i in gen_crvs_ini:
                gen_crvs.append(i)
    except:
        pass    
    #crv_gen_2=[] #   second generation curves
    try:
        clear_list(crv_gen_2)
    except:
        pass
    
    #crv_gen_3=[] #   second generation curves
    try:
        clear_list(crv_gen_3)
    except:
        pass
    try:
        clear_list(new_all_border_crvs)
    except:
        pass
    try:
        rs.DeleteObjects(new_all_border_crvs)
    except:
        pass
    try:
        rs.DeleteObjects(new_shaped_border_crvs_res_1)
    except:
        pass
    try:
        rs.DeleteObjects(new_shaped_border_crvs_res_2)
    except:
        pass
    try:
        rs.DeleteObjects(new_shaped_border_crvs_res_3)
    except:
        pass
    try:
        rs.DeleteObjects(temp_del_list_gen_ini_crvs)
    except:
        pass
    try:
        rs.DeleteObjects(temp_del_list_gen_crvs)
    except:
        pass
    try:
        rs.DeleteObjects(temp_del_list_gen_ini_crvs)
    except:
        pass
        
    rs.CopyObjects(temp_del_list_gen_ini_crvs,[1000,0,0])
    
    str_subdiv_ratio=[]
    r0=str_subdiv_ratio.append(subdiv_ratio1.Value/1000)
    str_subdiv_ratio.append(subdiv_ratio2.Value/1000)
    str_subdiv_ratio.append(subdiv_ratio2.Value/1000)
    
    
    gen=1
    crv=[]
    crv1=sub_div(crv_gen_1, gen, str_subdiv_ratio[gen])
    for i in crv1:
        if(i not in crv_gen_1):
            crv_gen_2.append(i)
            gen_crvs.append(i)
    
    gen=2
    crv2=[]
    subdiv_crvs=[]
    crv2=sub_div(crv_gen_2, gen, str_subdiv_ratio[gen])
    for i in crv2:
        if(i not in crv_gen_3):
            crv_gen_3.append(i)
            subdiv_crvs.append(i)
            gen_crvs.append(i)
    
    rs.DeleteObjects(temp_del_list_gen_crvs)
    for i in gen_crvs:
        #temp_del_list_gen_crvs.append(rs.AddPolyline(i))
        pass
    
    rs.DeleteObjects(temp_del_list_subdiv)
    for i in subdiv_crvs:
        if(i not in all_subdiv_crvs):
            all_subdiv_crvs.append(i)
            temp_del_list_subdiv.append(rs.AddPolyline(i))
    
    for i in temp_del_list_subdiv:
        shapeCross(i)
    rs.EnableRedraw(True)

def draw_showBorder():
    rs.EnableRedraw(False)
    #temp_del_list_line_border=[]
    try:
        rs.DeleteObjects(temp_del_list_line_border)
    except:
        pass
    try:
        rs.DeleteObjects(dummy_border_curves)
    except:
        pass
    try:
        clear_list(new_all_border_crvs)
    except:
        pass
    try:
        rs.DeleteObjects(new_shaped_border_crvs_res_1)
    except:
        pass
    try:
        rs.DeleteObjects(new_shaped_border_crvs_res_2)
    except:
        pass
    try:
        rs.DeleteObjects(new_shaped_border_crvs_res_3)
    except:
        pass
    if(temp_del_list_gen_ini_crvs is not None):
        rs.DeleteObjects(temp_del_list_gen_ini_crvs)
    if(temp_del_list_subdiv is not None):
        rs.DeleteObjects(temp_del_list_subdiv)
    if(temp_del_list_gen_crvs is not None):
        rs.DeleteObjects(temp_del_list_gen_crvs)
    for i in all_border_crv_pts:
        dummy_border_crvs.append(rs.AddPolyline(i))
    rs.EnableRedraw(True)

def makeBorder(new_crvs,gen, r):
    try:
        clear_list(all_border_crv_pts)
    except:
        pass
    for c in new_crvs:
        i=rs.AddPolyline(c)
        ccen=rs.CurveAreaCentroid(i)[0]
        j=rs.ScaleObject(i,ccen,[r,r,1],False)
        #j=rs.ScaleObject(i,ccen,[r,r,1],True)
        pts=rs.CurvePoints(j)
        if(pts not in all_border_crv_pts):
            all_border_crv_pts.append(pts)
        rs.DeleteObject(j)
    for i in all_border_crv_pts:
        new_all_border_crvs.append(rs.AddPolyline(i))

def draw_border(sender, e):
    rs.EnableRedraw(False)
        #all_border_crv_pts=[]
    try:
        clear_list(all_border_crv_pts)
    except:
        pass
        
    #crv_bor_0=[] #  initial border curve
    try:
        clear_list(crv_bor)
    except:
        pass
    
    #crv_bor_1=[] #  first border curve
    try:
        clear_list(crv_bor)
    except:
        pass
    
    #crv_bor_2=[] #  second border curve
    try:
        clear_list(crv_bor_2)
    except:
        pass
    
    #temp_del_list_line_border=[]
    try:
        rs.DeleteObjects(temp_del_list_line_border)
    except:
        pass
    
    #dummy_border_crvs
    try:
        rs.DeleteObjects(dummy_border_crvs)
        clear_list(dummy_border_crvs)
    except:
        pass
    
    #temp_del_list_L_border=[]
    try:
        rs.DeleteObjects(temp_del_list_L_border)
        clear_list(temp_del_list_L_border)
    except:
        pass
    #str_subdiv_ratio=[]
    try:
        clear_list(str_subdiv_ratio)
    except:
        pass
    
    #str_border_ratio=[]
    try:
        clear_list(str_border_ratio)
    except:
        pass
    
    #temp_del_list_border=[]
    try:
        rs.DeleteObjects(temp_del_list_border)
    except:
        pass
        
    #temp_del_list_border_line=[]
    try:
        rs.DeleteObjects(temp_del_list_border_line)
    except:
        pass
    try:
        rs.DeleteObjects(new_all_border_crvs)
    except:
        pass
    try:
        clear_list(new_all_border_crvs)
    except:
        pass
    try:
        rs.DeleteObjects(new_shaped_border_crvs_res_1)
    except:
        pass
    try:
        rs.DeleteObjects(new_shaped_border_crvs_res_2)
    except:
        pass
    try:
        rs.DeleteObjects(new_shaped_border_crvs_res_3)
    except:
        pass
    if(temp_del_list_gen_ini_crvs is not None):
        rs.DeleteObjects(temp_del_list_gen_ini_crvs)
    if(temp_del_list_gen_crvs is not None):
        rs.DeleteObjects(temp_del_list_gen_crvs)
    str_border_ratio=[]
    #str_border_ratio.append(bor_1.Value/1000)
    #str_border_ratio.append(0)
    #str_border_ratio.append(ui_border_ratio.Value/1000)
    #str_border_ratio.append(bor_3.Value/1000)
    bor_ratio=ui_border_ratio.Value/1000
    if(crv_gen_0 is not None):
        gen=1
        if(bor_1_yes.Checked==True):
            makeBorder(crv_gen_0, gen, bor_ratio*0.95) 
        else:
            pass
        gen=1
        if(bor_2_yes.Checked==True):
            makeBorder(crv_gen_1, gen, bor_ratio*1)
        else:
            pass
        gen=2
        if(bor_3_yes.Checked==True):
            makeBorder(crv_gen_2, gen, bor_ratio*1)
        else:
            pass
    for i in all_subdiv_crvs:
        temp_del_list_subdiv.append(rs.AddPolyline(i))
    for i in all_border_crv_pts:
        temp_del_list_border.append(rs.AddPolyline(i))
    rs.EnableRedraw(True)

def draw_canal_stage1(sender,e):
    rs.EnableRedraw(False)
    print("Canal _system")
    try:
        rs.DeleteObjects(dummy_canal_arms)
        clear_list(dummy_canal_arms)
    except:
        pass
    try:
        clear_list(canal_cen_pts)
    except:
        pass
    try:
        clear_list(dummy_canal_arm_pts)
    except:
        pass
    try:
        rs.DeleteObjects(temp_del_canal_arms)
    except:
        pass
    try:
        rs.DeleteObjects(canal_arm_gen_pts)
        clear_list(canal_arm_gen_pts)
    except:
        pass        
    try:
        rs.DeleteObjects(canal_arrows)
    except:
        pass
    try:
        rs.DeleteObjects(stage1_dummy_canal_arms)
    except:
        pass
    ar=math.sqrt(rs.CurveArea(site_crv)[0])/12
    if(can_1_yes.Checked==True):
        for i in crv_gen_0:
            crv_pts=i
            x0=crv_pts[0][0]
            y0=crv_pts[0][1]
            x1=crv_pts[1][0]
            y1=crv_pts[1][1]
            x2=crv_pts[2][0]
            y2=crv_pts[2][1]
            x3=crv_pts[3][0]
            y3=crv_pts[3][1]
            mx0=(x0+x1)/2
            my0=(y0+y1)/2
            mx1=(x1+x2)/2
            my1=(y1+y2)/2
            mx2=(x2+x3)/2
            my2=(y2+y3)/2
            mx3=(x3+x0)/2
            my3=(y3+y0)/2            
            d=(site_dim_a/4)/10
            stage1_dummy_canal_arms.append(rs.AddLine([mx0,my0+d,0],[mx2,my2-d,0]))
            stage1_dummy_canal_arms.append(rs.AddLine([mx1-d,my1,0],[mx3+d,my3,0]))
            
            arrow_len=10
            
            a1=rs.AddLine([mx0,my0+d,0],[mx0+arrow_len,my0+d,0])
            a2=rs.RotateObject(a1,[mx0,my0+d,0],60,[0,0,1],False)
            a3=rs.RotateObject(a1,[mx0,my0+d,0],60,[0,0,1],True)
            c=rs.AddPolyline([rs.CurveStartPoint(a2),rs.CurveEndPoint(a2),rs.CurveEndPoint(a3),rs.CurveStartPoint(a3)])
            canal_arrows.append(rs.AddHatch(c,'solid'))
            rs.DeleteObjects([a1,a2,a3,c])
            
            a4=rs.AddLine([mx2,my2-d,0],[mx2+arrow_len,my2-d,0])
            a5=rs.RotateObject(a4,[mx2,my2-d,0],-60,[0,0,1],False)
            a6=rs.RotateObject(a4,[mx2,my2-d,0],-60,[0,0,1],True)
            c1=rs.AddPolyline([rs.CurveStartPoint(a5),rs.CurveEndPoint(a5),rs.CurveEndPoint(a6),rs.CurveStartPoint(a6)])
            canal_arrows.append(rs.AddHatch(c1,'solid'))
            rs.DeleteObjects([a4,a5,a6,c1])
            
            a7=rs.AddLine([mx1-d,my1,0],[mx1+arrow_len-d,my1,0])
            a8=rs.RotateObject(a7,[mx1-d,my1,0],-60,[0,0,1],False)
            a9=rs.RotateObject(a7,[mx1-d,my1,0],-60,[0,0,1],True)
            c2=rs.AddPolyline([rs.CurveStartPoint(a8),rs.CurveEndPoint(a8),rs.CurveEndPoint(a9),rs.CurveStartPoint(a9)])
            c3=rs.RotateObject(c2,[mx1-d,my1,0],-90,[0,0,1],False)
            canal_arrows.append(rs.AddHatch(c3,'solid'))
            rs.DeleteObjects([a7,a8,a9,c2])
            
            a10=rs.AddLine([mx3+d,my3,0],[mx3+arrow_len+d,my3,0])
            a11=rs.RotateObject(a10,[mx3+d,my3,0],-60,[0,0,1],True)
            a12=rs.RotateObject(a11,[mx3+d,my3,0],-60,[0,0,1],True)
            c4=rs.AddPolyline([rs.CurveStartPoint(a11),rs.CurveEndPoint(a11),rs.CurveEndPoint(a12),rs.CurveStartPoint(a12)])
            c5=rs.RotateObject(c4,[mx3+d,my3,0],90,[0,0,1],False)
            canal_arrows.append(rs.AddHatch(c5,'solid'))
            rs.DeleteObjects([a10,a11,a12,c4])
            
    if(can_2_yes.Checked==True):
        for i in crv_gen_1:
            crv_pts=i
            x0=crv_pts[0][0]
            y0=crv_pts[0][1]
            x1=crv_pts[1][0]
            y1=crv_pts[1][1]
            x2=crv_pts[2][0]
            y2=crv_pts[2][1]
            x3=crv_pts[3][0]
            y3=crv_pts[3][1]
            mx0=(x0+x1)/2
            my0=(y0+y1)/2
            mx1=(x1+x2)/2
            my1=(y1+y2)/2
            mx2=(x2+x3)/2
            my2=(y2+y3)/2
            mx3=(x3+x0)/2
            my3=(y3+y0)/2
            stage1_dummy_canal_arms.append(rs.AddLine([mx0,my0,0],[mx2,my2,0]))
            stage1_dummy_canal_arms.append(rs.AddLine([mx1,my1,0],[mx3,my3,0]))
            
            arrow_len=7
            
            a1=rs.AddLine([mx0,my0,0],[mx0+arrow_len,my0,0])
            a2=rs.RotateObject(a1,[mx0,my0,0],60,[0,0,1],False)
            a3=rs.RotateObject(a1,[mx0,my0,0],60,[0,0,1],True)
            c=rs.AddPolyline([rs.CurveStartPoint(a2),rs.CurveEndPoint(a2),rs.CurveEndPoint(a3),rs.CurveStartPoint(a3)])
            canal_arrows.append(rs.AddHatch(c,'solid'))
            rs.DeleteObjects([a1,a2,a3,c])
            
            a4=rs.AddLine([mx2,my2,0],[mx2+arrow_len,my2,0])
            a5=rs.RotateObject(a4,[mx2,my2,0],-60,[0,0,1],False)
            a6=rs.RotateObject(a4,[mx2,my2,0],-60,[0,0,1],True)
            c1=rs.AddPolyline([rs.CurveStartPoint(a5),rs.CurveEndPoint(a5),rs.CurveEndPoint(a6),rs.CurveStartPoint(a6)])
            canal_arrows.append(rs.AddHatch(c1,'solid'))
            rs.DeleteObjects([a4,a5,a6,c1])
            
            a7=rs.AddLine([mx1,my1,0],[mx1+arrow_len,my1,0])
            a8=rs.RotateObject(a7,[mx1,my1,0],-60,[0,0,1],False)
            a9=rs.RotateObject(a7,[mx1,my1,0],-60,[0,0,1],True)
            c2=rs.AddPolyline([rs.CurveStartPoint(a8),rs.CurveEndPoint(a8),rs.CurveEndPoint(a9),rs.CurveStartPoint(a9)])
            c3=rs.RotateObject(c2,[mx1,my1,0],-90,[0,0,1],False)
            canal_arrows.append(rs.AddHatch(c3,'solid'))
            rs.DeleteObjects([a7,a8,a9,c2])
            
            a10=rs.AddLine([mx3,my3,0],[mx3+arrow_len,my3,0])
            a11=rs.RotateObject(a10,[mx3,my3,0],-60,[0,0,1],True)
            a12=rs.RotateObject(a11,[mx3,my3,0],-60,[0,0,1],True)
            c4=rs.AddPolyline([rs.CurveStartPoint(a11),rs.CurveEndPoint(a11),rs.CurveEndPoint(a12),rs.CurveStartPoint(a12)])
            c5=rs.RotateObject(c4,[mx3,my3,0],90,[0,0,1],False)
            canal_arrows.append(rs.AddHatch(c5,'solid'))
            rs.DeleteObjects([a10,a11,a12,c4])
            
    if(can_3_yes.Checked==True):
        for i in crv_gen_2:
            crv_pts=i
            x0=crv_pts[0][0]
            y0=crv_pts[0][1]
            x1=crv_pts[1][0]
            y1=crv_pts[1][1]
            x2=crv_pts[2][0]
            y2=crv_pts[2][1]
            x3=crv_pts[3][0]
            y3=crv_pts[3][1]
            mx0=(x0+x1)/2
            my0=(y0+y1)/2
            mx1=(x1+x2)/2
            my1=(y1+y2)/2
            mx2=(x2+x3)/2
            my2=(y2+y3)/2
            mx3=(x3+x0)/2
            my3=(y3+y0)/2
            stage1_dummy_canal_arms.append(rs.AddLine([mx0,my0 ,0],[mx2,my2 ,0]))
            stage1_dummy_canal_arms.append(rs.AddLine([mx1 ,my1,0],[mx3 ,my3,0]))
            
            arrow_len=5
            
            a1=rs.AddLine([mx0,my0,0],[mx0+arrow_len,my0,0])
            a2=rs.RotateObject(a1,[mx0,my0,0],60,[0,0,1],False)
            a3=rs.RotateObject(a1,[mx0,my0,0],60,[0,0,1],True)
            c=rs.AddPolyline([rs.CurveStartPoint(a2),rs.CurveEndPoint(a2),rs.CurveEndPoint(a3),rs.CurveStartPoint(a3)])
            canal_arrows.append(rs.AddHatch(c,'solid'))
            rs.DeleteObjects([a1,a2,a3,c])
            
            a4=rs.AddLine([mx2,my2,0],[mx2+arrow_len,my2,0])
            a5=rs.RotateObject(a4,[mx2,my2,0],-60,[0,0,1],False)
            a6=rs.RotateObject(a4,[mx2,my2,0],-60,[0,0,1],True)
            c1=rs.AddPolyline([rs.CurveStartPoint(a5),rs.CurveEndPoint(a5),rs.CurveEndPoint(a6),rs.CurveStartPoint(a6)])
            canal_arrows.append(rs.AddHatch(c1,'solid'))
            rs.DeleteObjects([a4,a5,a6,c1])
            
            a7=rs.AddLine([mx1,my1,0],[mx1+arrow_len,my1,0])
            a8=rs.RotateObject(a7,[mx1,my1,0],-60,[0,0,1],False)
            a9=rs.RotateObject(a7,[mx1,my1,0],-60,[0,0,1],True)
            c2=rs.AddPolyline([rs.CurveStartPoint(a8),rs.CurveEndPoint(a8),rs.CurveEndPoint(a9),rs.CurveStartPoint(a9)])
            c3=rs.RotateObject(c2,[mx1,my1,0],-90,[0,0,1],False)
            canal_arrows.append(rs.AddHatch(c3,'solid'))
            rs.DeleteObjects([a7,a8,a9,c2])
            
            a10=rs.AddLine([mx3,my3,0],[mx3+arrow_len,my3,0])
            a11=rs.RotateObject(a10,[mx3,my3,0],-60,[0,0,1],True)
            a12=rs.RotateObject(a11,[mx3,my3,0],-60,[0,0,1],True)
            c4=rs.AddPolyline([rs.CurveStartPoint(a11),rs.CurveEndPoint(a11),rs.CurveEndPoint(a12),rs.CurveStartPoint(a12)])
            c5=rs.RotateObject(c4,[mx3,my3,0],90,[0,0,1],False)
            canal_arrows.append(rs.AddHatch(c5,'solid'))
            rs.DeleteObjects([a10,a11,a12,c4])
            
    rs.EnableRedraw(True)

def indent_canal_arms(crvX,ny):
    try:
        rs.DeleteObjects(dummy_canal_arms)
    except:
        pass
    try:
        rs.DeleteObjects(dummy_canal_pl_crvs)
    except:
        pass
    c0=rs.CopyObject(site_crv,[0,0,0])
    c0pt=rs.CurvePoints(c0)
    diX=rs.Distance(c0pt[0],c0pt[1])/12
    diY=rs.Distance(c0pt[1],c0pt[2])/12
    ar=math.sqrt(rs.CurveArea(site_crv)[0])/12
    r0=(ar/200)*can_arm_1.Value
    r1=(ar/200)*can_arm_2.Value
    r2=(ar/200)*can_arm_3.Value
    #r2=(ar/200)*(diX/16.5)*7
    rs.DeleteObject(c0)
    crvXcen=rs.CurveAreaCentroid(crvX)[0]
    crvXpts=rs.CurvePoints(crvX)
    l1=rs.Distance(crvXpts[0],crvXpts[1])
    l2=rs.Distance(crvXpts[1],crvXpts[2])
    l01=rs.AddLine(crvXpts[0],crvXpts[1])
    l12=rs.AddLine(crvXpts[1],crvXpts[2])
    l23=rs.AddLine(crvXpts[2],crvXpts[3])
    l30=rs.AddLine(crvXpts[3],crvXpts[0])
    m01=rs.CurveMidPoint(l01)
    m12=rs.CurveMidPoint(l12)
    m23=rs.CurveMidPoint(l23)
    m30=rs.CurveMidPoint(l30)
    
    """
    rs.AddTextDot("m01",m01)
    rs.AddTextDot("m12",m12)
    rs.AddTextDot("m23",m23)
    rs.AddTextDot("m30",m30)
    rs.AddTextDot("0",crvXpts[0])
    rs.AddTextDot("1",crvXpts[1])
    rs.AddTextDot("2",crvXpts[2])
    rs.AddTextDot("3",crvXpts[3])
    """
    ####    initially r2 was original; now it is r1
    if(ny==1):
        pl1=rs.AddPolyline([m30,crvXpts[0],crvXpts[1],m12])
        off_pt=[m01[0],m01[1]+500,0]
        pl2=rs.OffsetCurve(pl1,off_pt,r1)
        pl3=rs.AddPolyline([rs.CurveStartPoint(pl1),rs.CurveStartPoint(pl2)])
        pl4=rs.AddPolyline([rs.CurveEndPoint(pl1),rs.CurveEndPoint(pl2)])
        pl=rs.JoinCurves([pl1,pl2,pl3,pl4])
        det_canal_ends.append(pl)
        rs.DeleteObjects([pl1,pl2,pl3,pl4])
    if(ny==2):
        pl1=rs.AddPolyline([m30,crvXpts[3],crvXpts[2],m12])
        off_pt=[m23[0],m23[1]-500,0]
        pl2=rs.OffsetCurve(pl1,off_pt,r1)
        pl3=rs.AddPolyline([rs.CurveStartPoint(pl1),rs.CurveStartPoint(pl2)])
        pl4=rs.AddPolyline([rs.CurveEndPoint(pl1),rs.CurveEndPoint(pl2)])
        pl=rs.JoinCurves([pl1,pl2,pl3,pl4])
        det_canal_ends.append(pl)
        rs.DeleteObjects([pl1,pl2,pl3,pl4])
    if(ny==3):
        pl1=rs.AddPolyline([m01,crvXpts[1],crvXpts[2],m23])
        off_pt=[m01[0]-500,m01[1],0]
        pl2=rs.OffsetCurve(pl1,off_pt,r1)
        pl3=rs.AddPolyline([rs.CurveStartPoint(pl1),rs.CurveStartPoint(pl2)])
        pl4=rs.AddPolyline([rs.CurveEndPoint(pl1),rs.CurveEndPoint(pl2)])
        pl=rs.JoinCurves([pl1,pl2,pl3,pl4])
        det_canal_ends.append(pl)
        rs.DeleteObjects([pl1,pl2,pl3,pl4])
    if(ny==4):
        pl1=rs.AddPolyline([m01,crvXpts[0],crvXpts[3],m23])
        off_pt=[m30[0]+500,m30[1],0]
        pl2=rs.OffsetCurve(pl1,off_pt,r1)
        pl3=rs.AddPolyline([rs.CurveStartPoint(pl1),rs.CurveStartPoint(pl2)])
        pl4=rs.AddPolyline([rs.CurveEndPoint(pl1),rs.CurveEndPoint(pl2)])
        pl=rs.JoinCurves([pl1,pl2,pl3,pl4])
        det_canal_ends.append(pl)
        rs.DeleteObjects([pl1,pl2,pl3,pl4])
        
    temp=[]
    temp1=[]
    temp2=[]
    
    for i in final_canal_sys:
        if rs.IsCurve(i):
            m=rs.CurveCurveIntersection(i,crvX)
            if(m is not None):
                temp1.append(rs.CurveBooleanDifference(i,crvX))
                temp.append(i)
    rs.DeleteObjects(temp)
    
    for i in temp1:
        final_canal_sys.append(i)
    
    rs.DeleteObject(l01)
    rs.DeleteObject(l12)
    rs.DeleteObject(l23)
    rs.DeleteObject(l30)
    #rs.DeleteObject(crvX)

def modulate_canal_arm(crvX):
    plY=[]
    for j in def_canal_arms:
        if(rs.IsCurve(j)):
            m=rs.CurveCurveIntersection(j,crvX)
            if(m is not None):
                crvY=rs.CurveBooleanDifference(j,crvX)
                idx=def_canal_arms.index(j)
                def_canal_arms.insert(idx,crvY)
                rs.DeleteObject(j)
                break
            else:
                pass
    rs.DeleteObject(crvX)
    return plY

def modulate_line_border_boolean():
    temp=[]
    for i in bool_crvs:
        sum=0
        for j in line_border_crvs:
            if(rs.IsCurve(i) and rs.IsCurve(j)):
                sp=rs.CurveStartPoint(j)
                ep=rs.CurveEndPoint(j)
                u=rs.CurveCurveIntersection(j,i)
                if(u is not None):
                    sum+=1
                    d1=rs.Distance(sp,u[0][1])
                    d2=rs.Distance(ep,u[0][1])
                    if(d1>d2):
                        idx=line_border_crvs.index(j)
                        l1=rs.AddLine(u[0][1],sp)
                        temp.append(l1)
                        line_border_crvs.insert(idx,l1)
                        rs.DeleteObject(j)
                    else:
                        idx=line_border_crvs.index(j)
                        l1=rs.AddLine(u[0][1],ep)
                        temp.append(l1)
                        line_border_crvs.insert(idx,l1)
                        rs.DeleteObject(j)
    for i in temp:
        if(i not in line_border_crvs):
            line_border_crvs.append(i)
    
    temp=[]
    for i in line_border_crvs:
        if(rs.IsCurve(i)):
            sp1=rs.CurveStartPoint(i)
            ep1=rs.CurveStartPoint(i)
            d1=rs.Distance(sp1,ep1)
            for j in line_border_crvs:
                if(rs.IsCurve(j)):
                    sp2=rs.CurveStartPoint(j)
                    ep2=rs.CurveStartPoint(j)
                    d2=rs.Distance(sp2,ep2)
                    if(d2>d1 and (rs.Distance(ep1,ep2)<0.0001)):
                        line_border_crvs.remove(j)
                        rs.DeleteObject(j)

def draw_refineBorder(sender, e):
    rs.EnableRedraw(False)
    try:
        rs.DeleteObjects(dummy_border_curves)
    except:
        pass
    rs.DeleteObjects(temp_del_list_subdiv)
    rs.DeleteObjects(temp_del_list_border)
    border_crvs=trimBorder(all_subdiv_crvs,all_border_crv_pts)
    for i in border_crvs:
        shaped_border_crvs.append(i)
    for i in shaped_border_crvs[0]:
        temp_del_list_border.append(rs.AddPolyline(i))
    for i in shaped_border_crvs[1]:
        temp_del_list_border.append(rs.AddPolyline(i))
    for i in all_subdiv_crvs:
        temp_del_list_subdiv.append(rs.AddPolyline(i))
    rs.EnableRedraw(True)

def draw_canal(sender,e):
    try:
        rs.DeleteObjects(stage1_dummy_canal_arms)
    except:
        pass
    try:
        rs.DeleteObjects(def_canal_arms)
        #clear_list(def_canal_arms)
    except:
        pass
    
    try:
        rs.DeleteObjects(canal_pl)
        #clear_list(canal_pl)
    except:
        pass
    
    try:
        clear_list(canal_pl_pts)
    except:
        pass
    
    try:
        rs.DeleteObjects(temp_del_list_subdiv)
    except:
        pass
    try:
        rs.DeleteObjects(temp_del_list_border)
    except:
        pass
    try:
        clear_list(def0_canal_arm)
        #rs.DeleteObjects(def0_canal_arm)
    except:
        pass
    try:
        rs.DeleteObjects(tmp0.indent)
        clear_list(tmp0.indent)
    except:
        pass
    #dummy_canal_arms=[]
    try:
        rs.DeleteObjects(dummy_canal_arms)
        clear_list(dummy_canal_arms)
    except:
        pass
    rs.EnableRedraw(False)
    p1=rs.AddPoint(all_subdiv_crvs[0][0])
    p2=rs.AddPoint(all_subdiv_crvs[0][1])
    p3=rs.AddPoint(all_subdiv_crvs[0][2])
    diX0=rs.Distance(p1,p2)
    diY0=rs.Distance(p2,p3)
    rs.DeleteObject(p1)
    rs.DeleteObject(p2)
    rs.DeleteObject(p3)
    
    r1=can_1.Value/25
    r2=can_2.Value/25
    #r3=can_3.Value
    
    c0=rs.AddPolyline(crv_gen_0[0])
    c1=rs.AddPolyline(crv_gen_1[0])
    c2=rs.AddPolyline(crv_gen_1[1])
    c3=rs.AddPolyline(crv_gen_1[2])
    c4=rs.AddPolyline(crv_gen_1[3])
    
    canal_gen=0
    diX=rs.Distance(all_border_crv_pts[0][0],all_subdiv_crvs[0][1])
    diY=rs.Distance(all_border_crv_pts[0][1],all_subdiv_crvs[0][2])
    canal_pl.append(main_canal_sys(c0, canal_gen, diX, diY,0,r1))
    
    canal_gen=1
    canal_pl.append(main_canal_sys(c1, canal_gen,diX,diY,1,r2))
    canal_pl.append(main_canal_sys(c2, canal_gen,diX,diY,2,r2))
    canal_pl.append(main_canal_sys(c3, canal_gen,diX,diY,3,r2))
    canal_pl.append(main_canal_sys(c4, canal_gen,diX,diY,4,r2))
    rs.DeleteObject(c0)
    rs.DeleteObject(c1)
    rs.DeleteObject(c2)
    rs.DeleteObject(c3)
    rs.DeleteObject(c4)
    
    ############################################
    ####    preferred internal canals   ####
    
    c5=rs.AddPolyline(crv_gen_2[0])
    c7=rs.AddPolyline(crv_gen_2[2])
    c11=rs.AddPolyline(crv_gen_2[6])
    c13=rs.AddPolyline(crv_gen_2[8])
    c15=rs.AddPolyline(crv_gen_2[10])
    c17=rs.AddPolyline(crv_gen_2[12])
    c21=rs.AddPolyline(crv_gen_2[16])
    c23=rs.AddPolyline(crv_gen_2[18])
    
    canal_gen=2
    canal_pl.append(main_canal_sys(c5, canal_gen,diX,diY,5,r2*.65))
    canal_pl.append(main_canal_sys(c7, canal_gen,diX,diY,5,r2*.65))
    canal_pl.append(main_canal_sys(c11, canal_gen,diX,diY,5,r2*.65))
    canal_pl.append(main_canal_sys(c13, canal_gen,diX,diY,5,r2*.65))
    canal_pl.append(main_canal_sys(c15, canal_gen,diX,diY,5,r2*.65))
    canal_pl.append(main_canal_sys(c17, canal_gen,diX,diY,5,r2*.65))
    canal_pl.append(main_canal_sys(c21, canal_gen,diX,diY,5,r2*.65))
    canal_pl.append(main_canal_sys(c23, canal_gen,diX,diY,5,r2*.65))
    
    rs.DeleteObject(c5)
    rs.DeleteObject(c6)
    rs.DeleteObject(c11)
    rs.DeleteObject(c13)
    rs.DeleteObject(c15)
    rs.DeleteObject(c17)
    rs.DeleteObject(c21)
    rs.DeleteObject(c23)
    
    ############################################
    ####     extra internal central canals   ####
    
    c6=rs.AddPolyline(crv_gen_2[1])
    c8=rs.AddPolyline(crv_gen_2[3])
    #c9=rs.AddPolyline(crv_gen_2[4])
    c10=rs.AddPolyline(crv_gen_2[5])
    c12=rs.AddPolyline(crv_gen_2[7])
    #c14=rs.AddPolyline(crv_gen_2[9])
    c15=rs.AddPolyline(crv_gen_2[10])
    c16=rs.AddPolyline(crv_gen_2[11])
    c18=rs.AddPolyline(crv_gen_2[13])
    #c19=rs.AddPolyline(crv_gen_2[14])
    c20=rs.AddPolyline(crv_gen_2[15])
    c22=rs.AddPolyline(crv_gen_2[17])
    #c24=rs.AddPolyline(crv_gen_2[19])
    #c25=rs.AddPolyline(crv_gen_2[20])
    
    canal_pl.append(main_canal_sys(c6, canal_gen,diX,diY,5))
    canal_pl.append(main_canal_sys(c8, canal_gen,diX,diY,5))
    canal_pl.append(main_canal_sys(c9, canal_gen,diX,diY,5))
    #canal_pl.append(main_canal_sys(c10, canal_gen,diX,diY,5))
    canal_pl.append(main_canal_sys(c12, canal_gen,diX,diY,5))
    #canal_pl.append(main_canal_sys(c14, canal_gen,diX,diY,5))
    canal_pl.append(main_canal_sys(c16, canal_gen,diX,diY,5))
    canal_pl.append(main_canal_sys(c18, canal_gen,diX,diY,5))
    #canal_pl.append(main_canal_sys(c19, canal_gen,diX,diY,5))
    canal_pl.append(main_canal_sys(c20, canal_gen,diX,diY,5))
    canal_pl.append(main_canal_sys(c22, canal_gen,diX,diY,5))
    #canal_pl.append(main_canal_sys(c24, canal_gen,diX,diY,5))
    #canal_pl.append(main_canal_sys(c25, canal_gen,diX,diY,5))


    rs.DeleteObject(c8)
    #rs.DeleteObject(c9)
    rs.DeleteObject(c10)
    rs.DeleteObject(c12)
    rs.DeleteObject(c13)
    #rs.DeleteObject(c14)
    rs.DeleteObject(c15)
    rs.DeleteObject(c16)
    rs.DeleteObject(c17)
    rs.DeleteObject(c18)
    rs.DeleteObject(c20)
    
    ############################################
    
    rs.DeleteObjects(temp_del_list_border)
    rs.DeleteObjects(temp_del_list_subdiv)
    temp=plot_canal_arms(diX,diY,diX0,diY0)
    for i in temp:
        def_canal_arms.append(rs.AddPolyline(i))
    for i in all_subdiv_crvs:
        temp_del_list_subdiv.append(rs.AddPolyline(i))
    #for i in shaped_border_crvs[0]:
        #temp_del_list_border.append(rs.AddPolyline(i))
    rs.EnableRedraw(True)

def draw_canal_ends(sender,e):
    rs.EnableRedraw(False)
    try:
        rs.DeleteObjects(shape_cross)
    except:
        pass
    try:
        rs.DeleteObjects(stage1_dummy_canal_arms)
    except:
        pass
    try:
        rs.DeleteObjects(tmp0_indent)
    except:
        pass
    try:
        rs.DeleteObjects(user_indent_points)
    except:
        pass
    try:
        rs.DeleteObjects(del_pts_index)
    except:
        pass
    try:
        rs.DeleteObjects(temp_del_list_subdiv)
    except:
        pass
    try:
        rs.DeleteObjects(temp_del_list_border)
    except:
        pass
    try:
        rs.DeleteObjects(temp_del_list_L_border)
    except:
        pass
    try:
        rs.DeleteObjects(temp_del_list_line_border)
    except:
        pass
    try:
        rs.DeleteObjects(global_line_border)
    except:
        pass
    c0=rs.CopyObject(site_crv,[0,0,0])
    site_cen=rs.CurveAreaCentroid(c0)[0]
    c0pt=rs.CurvePoints(c0)
    diX=rs.Distance(c0pt[0],c0pt[1])/12
    diY=rs.Distance(c0pt[1],c0pt[2])/12
    ar=math.sqrt(rs.CurveArea(c0)[0])/20
    if(can_arm_1.Value>1.5):
        r0=(ar/200)*can_arm_1.Value
    else:
        r0=(ar/200)*20
    if(can_arm_2.Value>1.5):
        r1=(ar/200)*can_arm_2.Value
    else:
        r1=(ar/200)*15
    if(can_arm_3.Value>1.5):
        r2=(ar/200)*can_arm_3.Value
    else:
        r2=(ar/200)*10
    rs.DeleteObject(c0) 
    
    k=0
    for i in canal_arm_gen_pts:
        #rs.AddTextDot(k,i)
        k+=1
        
    if(can_1_yes.Checked==True):
        ### mandatory indentation
        pt0=[canal_arm_gen_pts[0][0], canal_arm_gen_pts[0][1],0]
        crvX0= spl_modulate(pt0,2, r0, r0/3, 2,diX,diY,1,1)
        temp=[]
        temp1=[]
        for i in final_canal_sys:
            if rs.IsCurve(i):
                m=rs.CurveCurveIntersection(i,crvX0)
                if(m is not None):
                    temp1.append(rs.CurveBooleanDifference(i,crvX0))
                    temp.append(i)
                rs.DeleteObjects(temp)
        for i in temp1:
            final_canal_sys.append(i)
        indent_canal_arms(crvX0,11)
        
        pt1=[canal_arm_gen_pts[1][0], canal_arm_gen_pts[1][1],0]
        crvX1= spl_modulate(pt1,2, r0, r0/3, 2,diX,diY,1,1)
        temp=[]
        temp1=[]
        for i in final_canal_sys:
            if rs.IsCurve(i):
                m=rs.CurveCurveIntersection(i,crvX1)
                if(m is not None):
                    temp1.append(rs.CurveBooleanDifference(i,crvX1))
                    temp.append(i)
                rs.DeleteObjects(temp)
        for i in temp1:
            final_canal_sys.append(i)
        indent_canal_arms(crvX1,12)
        
        pt2=[canal_arm_gen_pts[2][0], canal_arm_gen_pts[2][1],0]
        crvX2= spl_modulate(pt2,2, r0/3, r0, 2,diX,diY,1,1)
        temp=[]
        temp1=[]
        for i in final_canal_sys:
            if rs.IsCurve(i):
                m=rs.CurveCurveIntersection(i,crvX2)
                if(m is not None):
                    temp1.append(rs.CurveBooleanDifference(i,crvX2))
                    temp.append(i)
                rs.DeleteObjects(temp)
        for i in temp1:
            final_canal_sys.append(i)
        indent_canal_arms(crvX2,13)
        
        pt3=[canal_arm_gen_pts[3][0], canal_arm_gen_pts[3][1],0]
        crvX3= spl_modulate(pt3,2, r0/3, r0, 2,diX,diY,1,1)
        temp=[]
        temp1=[]
        for i in final_canal_sys:
            if rs.IsCurve(i):
                m=rs.CurveCurveIntersection(i,crvX3)
                if(m is not None):
                    temp1.append(rs.CurveBooleanDifference(i,crvX3))
                    temp.append(i)
                rs.DeleteObjects(temp)
        for i in temp1:
            final_canal_sys.append(i)
        indent_canal_arms(crvX3,14)
        
        rs.DeleteObjects([crvX0,crvX1,crvX2,crvX3])

        if(can_2_yes.Checked==True):
            ### horizontal indentation
            if(can_det_hor.Checked==True):
                pt5=[canal_arm_gen_pts[5][0], canal_arm_gen_pts[5][1],0]
                crvX5= modulate2(pt5,2, r0, r0/3, 2,diX,diY,2,5)    
                indent_canal_arms(crvX5,1)
                
                pt9=[canal_arm_gen_pts[9][0], canal_arm_gen_pts[9][1],0]
                crvX9= modulate2(pt9,2, r0, r0/3, 2,diX,diY,2,9)
                indent_canal_arms(crvX9,1)
                
                
                pt16=[canal_arm_gen_pts[16][0], canal_arm_gen_pts[16][1],0]
                crvX16= modulate2(pt16,2, r0, r0/3, 2,diX,diY,2,16)
                indent_canal_arms(crvX16,2)
                
                pt12=[canal_arm_gen_pts[12][0], canal_arm_gen_pts[12][1],0]
                crvX12= modulate2(pt12,2, r0, r0/3, 2,diX,diY,2,12)
                indent_canal_arms(crvX12,2)
                
                rs.DeleteObjects([crvX5,crvX9,crvX12,crvX16])
            
            ### vertical indentation
            if(can_det_ver.Checked==True):
                pt15=[canal_arm_gen_pts[15][0], canal_arm_gen_pts[15][1],0]
                crvX15= modulate2(pt15,2, r0/3, r0, 2,diX,diY,2,15)
                indent_canal_arms(crvX15,3)
                
                pt11=[canal_arm_gen_pts[11][0], canal_arm_gen_pts[11][1],0]
                crvX11= modulate2(pt11,2, r0/3, r0, 2,diX,diY,2,11)
                indent_canal_arms(crvX11,3)
                
                pt18=[canal_arm_gen_pts[18][0], canal_arm_gen_pts[18][1],0]
                crvX18= modulate2(pt18,2, r0/3, r0, 2,diX,diY,2,18)
                indent_canal_arms(crvX18,4)
                
                pt6=[canal_arm_gen_pts[6][0], canal_arm_gen_pts[6][1],0]
                crvX6= modulate2(pt6,2, r0/3, r0, 2,diX,diY,2,6)
                indent_canal_arms(crvX6,4)
                
                rs.DeleteObjects([crvX15,crvX11,crvX18,crvX6])
        else:
            pass
    if(can_1_yes.Checked==False):
        if(can_2_yes.Checked==True):
            ### horizontal indentation
            try:
                if(can_det_hor.Checked==True):
                    pt1=[canal_arm_gen_pts[1][0], canal_arm_gen_pts[1][1],0]
                    crvX1= modulate2(pt1,2, r0/1.25, r0/3, 2,diX,diY,2,1.1)    
                    indent_canal_arms(crvX1,1)
                    
                    pt5=[canal_arm_gen_pts[5][0], canal_arm_gen_pts[5][1],0]
                    crvX5= modulate2(pt5,2, r0/1.25, r0/3, 2,diX,diY,2,5.1)
                    indent_canal_arms(crvX5,1)
                    
                    
                    pt12=[canal_arm_gen_pts[12][0], canal_arm_gen_pts[12][1],0]
                    crvX12= modulate2(pt12,2, r0/1.25, r0/3, 2,diX,diY,2,12.1)
                    indent_canal_arms(crvX12,2)
                    
                    pt8=[canal_arm_gen_pts[8][0], canal_arm_gen_pts[8][1],0]
                    crvX8= modulate2(pt8,2, r0/1.25, r0/3, 2,diX,diY,2,8.1)
                    indent_canal_arms(crvX8,2)
                    
                    rs.DeleteObjects([crvX1,crvX5,crvX12,crvX8])
            except:
                pass    
                
            ### vertical indentation
            try:
                if(can_det_ver.Checked==True):
                    pt11=[canal_arm_gen_pts[11][0], canal_arm_gen_pts[11][1],0]
                    crvX11= modulate2(pt11,2, r0/3, r0/1.5, 2,diX,diY,2,11.1)
                    indent_canal_arms(crvX11,3)
                    
                    pt7=[canal_arm_gen_pts[7][0], canal_arm_gen_pts[7][1],0]
                    crvX7= modulate2(pt7,2, r0/3, r0/1.5, 2,diX,diY,2,7.1)
                    indent_canal_arms(crvX7,3)
                    
                    pt14=[canal_arm_gen_pts[14][0], canal_arm_gen_pts[14][1],0]
                    crvX14= modulate2(pt14,2, r0/3, r0/1.5, 2,diX,diY,2,14.1)
                    indent_canal_arms(crvX14,4)
                    
                    pt2=[canal_arm_gen_pts[2][0], canal_arm_gen_pts[2][1],0]
                    crvX2= modulate2(pt2,2, r0/3, r0/1.5, 2,diX,diY,2,2.1)
                    indent_canal_arms(crvX2,4)
                    
                    rs.DeleteObjects([crvX11,crvX7,crvX14,crvX2])
            except:
                pass
        else:
            pass
    else:
        pass
    for i in bool_crvs:
        if(rs.IsCurve(i)):
            shapeCross(i)
    for i in all_subdiv_crvs:
        c=rs.AddPolyline(i)
        shapeCross(c)
        temp_del_list_subdiv.append(c)
    rs.EnableRedraw(True)

def modulate2(xpt,n,rx,ry,req,diX,diY,detail_2,loc):
    #rs.EnableRedraw(False)
    try:
        rs.DeleteObjects(crvX)
    except:
        pass
    xx0=xpt[0]
    yy0=xpt[1]
    res=res_ratio.Value/50.0
    diX_this=(1*diX/5)*rx*res
    diY_this=(1*diY/5)*ry*res
    pt=[]
    if(req==1):
        pt.append( [ xx0-(diX_this),   yy0+(diY_this/2),  0] )  #0
        pt.append( [ xx0-(diX_this/2), yy0+(diY_this),    0] )  #1
        pt.append( [ xx0+(diX_this/2), yy0+(diY_this),    0] )  #2
        pt.append( [ xx0+(diX_this),   yy0+(diY_this/2),  0] )  #3
        pt.append( [ xx0+diX_this,     yy0-(diY_this/2),  0] )  #4
        pt.append( [ xx0+(diX_this/2), yy0-(diY_this),    0] )  #5
        pt.append( [ xx0-(diX_this/2), yy0-(diY_this),    0] )  #6
        pt.append( [ xx0-(diX_this),   yy0-(diY_this/2),  0] )  #7
        pt.append( [ xx0-(diX_this),   yy0+(diY_this/2),  0] )  #8
        crvX=rs.AddPolyline(pt)
    elif(req==7):
        crvX=rs.AddCircle(xpt,diX)
    else:
        pt.append([xx0-diX_this, yy0-diY_this,0])
        pt.append([xx0+diX_this,yy0-diY_this,0])
        pt.append([xx0+diX_this,yy0+diY_this,0])
        pt.append([xx0-diX_this,yy0+diY_this,0])
        pt.append([xx0-diX_this,yy0-diY_this,0])
        crvX=rs.AddPolyline(pt)

    crvcen=rs.CurveAreaCentroid(crvX)[0]
    ####    offset the central curves
    diX2=diX/3.5
    diX3=diX/2.475
    diX4=diX/1.775
    crvX_off=rs.OffsetCurve(crvX,[pt[0][0]-10000,pt[0][1],0],diX2)
    crvX_off1=rs.OffsetCurve(crvX,[pt[0][0]-10000,pt[0][1],0],diX3)
    crvX_off2=rs.OffsetCurve(crvX,[pt[0][0]-10000,pt[0][1],0],diX4)
    
    #   affect subdiv curves

    temp=[]
    for i in all_subdiv_crvs:
        c=rs.AddPolyline(i)
        m=rs.CurveCurveIntersection(c,crvX_off)
        if(m is not None):
            bx=rs.CurveBooleanDifference(c,crvX_off)
            bool_crvs.append(bx)
            temp.append(i)
        rs.DeleteObject(c)
    for i in temp:
        all_subdiv_crvs.remove(i)
    clear_list(temp)
    
    ####    cut the border_curve with crvX_off1
    ar0=rs.CurveArea(site_crv)[0]
    try:
        rs.DeleteObjects(temp1)
    except:
        pass
    temp1=[]
    k=0
    
    for i in new_all_border_crvs:
        ar1=rs.CurveArea(rs.coercecurve(i))[0]
        if(ar0/ar1 >16):#the smallest border
            m=rs.CurveCurveIntersection(rs.coercecurve(i),crvX_off1)
            if(m is not None):
                bx=rs.CurveBooleanDifference(rs.coercecurve(i),crvX_off1)
                #new_shaped_border_crvs_res_1.append(bx)
                temp1.append(i)
                new_all_border_crvs.insert(k,bx)
                new_all_border_crvs.remove(i)
        if(ar0/ar1 >4 and ar0/ar1 <8):#the smallest border
            m=rs.CurveCurveIntersection(rs.coercecurve(i),crvX_off2)
            if(m is not None):
                bx=rs.CurveBooleanDifference(rs.coercecurve(i),crvX_off2)
                #new_shaped_border_crvs_res_1.append(bx)
                temp1.append(i)
                new_all_border_crvs.insert(k,bx)
                new_all_border_crvs.remove(i)
        k+=1
    rs.DeleteObjects(temp1)
    
    
    
    #   find bool_crvs and affect it
    temp_bx=[]#boolean curve that contains L_border curves
    for c in bool_crvs:
        if(rs.IsCurve(c)):
            m=rs.CurveCurveIntersection(c,crvX_off)
            if(m is not None):
                bx=rs.CurveBooleanDifference(c,crvX_off)
                temp_bx.append(bx)
                rs.DeleteObject(c)
                bx_cen=rs.CurveAreaCentroid(bx)[0]
    #   find the closest L_border_crv
    for i in temp_bx:
        if(i not in bool_crvs):
            bool_crvs.append(i)
    ###     Deletes the first L-Border Curve wrt crvX_off1 from opposite side
    temp_l=[]#L_border curves
    temp_m=[]
    temp_del=[]
    try:
        for i in shaped_border_crvs[0]:
            temp_l.append(i)
        for i in temp_bx:
            for j in temp_l:
                c=rs.AddPolyline(processLcurve(j))
                m=rs.CurveCurveIntersection(i,c)
                if(m is not None):
                    y=rs.CurveBooleanIntersection(c,i)
                    temp_m.append(y)
                    temp_del.append(j)
                rs.DeleteObject(c)
        for i in temp_del:
            shaped_border_crvs[0].remove(i)
        li=[]
        k=0
        for i in temp_m:
            ar=rs.CurveArea(i)[0]
            li.append([i,ar])
            #pt=rs.CurveAreaCentroid(i)[0]
            #rs.AddTextDot(k,pt)
            k+=1
        lix=sorted(li,key=operator.itemgetter(1))
        #print(str(len(lix))+" : "+str(detail_2))
        if(len(lix)==4):
            if(detail_2==1):
                g1=lix[0][0]
                g2=lix[1][0]
                g3=lix[2][0]
                g4=lix[3][0]
                k1=rs.CurveBooleanDifference(g1,crvX_off2)
                k2=rs.CurveBooleanDifference(g2,crvX_off2)
                k3=rs.CurveBooleanDifference(g3,crvX_off1)
                k4=rs.CurveBooleanDifference(g4,crvX_off1)
                bool_crvs.append(k1)
                bool_crvs.append(k2)
                bool_crvs.append(k3)
                bool_crvs.append(k4)
                rs.DeleteObjects([g1,g2,g3,g4])
            elif(detail_2==2):
                temp_p=[]
                g1=lix[0][0]
                g2=lix[1][0]
                k1=rs.CurveBooleanDifference(g1,crvX_off1)                
                k2=rs.CurveBooleanDifference(g2,crvX_off1)
                spl_modulate(xpt,k1,loc,diX,diX2,diX3,diX4)
                spl_modulate(xpt,k2,loc,diX,diX2,diX3,diX4)
                bool_crvs.append(k1)
                bool_crvs.append(k2)
                rs.DeleteObjects([g1,g2])
            else:
                pass
        elif(len(lix)==2):
            if(detail_2==1):
                g1=lix[0][0]
                g2=lix[1][0]
                if(bor_3.Value<2 and ui_border_ratio.Value>2):
                    k1=rs.CurveBooleanDifference(g1,crvX_off2)
                    k2=rs.CurveBooleanDifference(g2,crvX_off2)
                elif(bor_3.Value>2 and ui_border_ratio.Value<2):
                    k1=rs.CurveBooleanDifference(g1,crvX_off1)
                    k2=rs.CurveBooleanDifference(g2,crvX_off1)
                elif(bor_3.Value>2 and bor_1.Value<2):
                    k1=rs.CurveBooleanDifference(g1,crvX_off1)
                    k2=rs.CurveBooleanDifference(g2,crvX_off1)
                else:
                    k1=rs.CurveBooleanDifference(g1,crvX_off1)
                    k2=rs.CurveBooleanDifference(g2,crvX_off1)
                spl_modulate(xpt,k1,loc,diX,diX2,diX3,diX4)
                spl_modulate(xpt,k2,loc,diX,diX2,diX3,diX4)
                bool_crvs.append(k1)
                bool_crvs.append(k2)
                rs.DeleteObjects([g1,g2])
            elif(detail_2==2):
                temp_p=[]
                g1=lix[0][0]
                g2=lix[1][0]
                if(bor_3.Value<2 and ui_border_ratio.Value>2):
                    k1=rs.CurveBooleanDifference(g1,crvX_off2)
                    k2=rs.CurveBooleanDifference(g2,crvX_off2)
                elif(bor_3.Value>2 and ui_border_ratio.Value<2):
                    k1=rs.CurveBooleanDifference(g1,crvX_off1)
                    k2=rs.CurveBooleanDifference(g2,crvX_off1)
                elif(bor_3.Value>2 and bor_1.Value<2):
                    k1=rs.CurveBooleanDifference(g1,crvX_off1)
                    k2=rs.CurveBooleanDifference(g2,crvX_off1)
                else:
                    #print('loc',loc)
                    k1=rs.CurveBooleanDifference(g1,crvX_off1)
                    k2=rs.CurveBooleanDifference(g2,crvX_off1)
                spl_modulate(xpt,k1,loc,diX,diX2,diX3,diX4)
                spl_modulate(xpt,k2,loc,diX,diX2,diX3,diX4)
                bool_crvs.append(k1)
                bool_crvs.append(k2)
                rs.DeleteObjects([g1,g2])
            else:
                pass
        else:
             pass
        #when only 1 border curve is present
        if(bor_1.Value<2 and ui_border_ratio.Value>2 and bor_3.Value<2 and can_arm_1.Value>2 and can_arm_2.Value>2):
            li=[]
            #rs.AddCircle(xpt,10)
            for c in bool_crvs:
                if(rs.IsCurve(c)):
                    c_cen=rs.CurveAreaCentroid(c)[0]
                    di=rs.Distance(c_cen,xpt)
                    li.append([c,di])
            del_loc=[0,1,2,3]
            if(loc not in del_loc):
                lix=sorted(li,key=operator.itemgetter(1))
                spl_modulate(xpt,lix[0][0],loc,diX,diX2,diX3,diX4)
                spl_modulate(xpt,lix[1][0],loc,diX,diX2,diX3,diX4)
    except:
        pass
    
    

    rs.DeleteObjects([crvX_off, crvX_off1, crvX_off2])
    #rs.EnableRedraw(True)
    return crvX

def spl_modulate(xpt,n,rx,ry,req,diX,diY,detail_2,loc):
    #rs.EnableRedraw(False)
    try:
        rs.DeleteObjects(crvX)
    except:
        pass
    xx0=xpt[0]
    yy0=xpt[1]
    res=res_ratio.Value/50.0
    diX_this=(1*diX/5)*rx*res
    diY_this=(1*diY/5)*ry*res
    pt=[]
    if(req==1):
        pt.append( [ xx0-(diX_this),   yy0+(diY_this/2),  0] )  #0
        pt.append( [ xx0-(diX_this/2), yy0+(diY_this),    0] )  #1
        pt.append( [ xx0+(diX_this/2), yy0+(diY_this),    0] )  #2
        pt.append( [ xx0+(diX_this),   yy0+(diY_this/2),  0] )  #3
        pt.append( [ xx0+diX_this,     yy0-(diY_this/2),  0] )  #4
        pt.append( [ xx0+(diX_this/2), yy0-(diY_this),    0] )  #5
        pt.append( [ xx0-(diX_this/2), yy0-(diY_this),    0] )  #6
        pt.append( [ xx0-(diX_this),   yy0-(diY_this/2),  0] )  #7
        pt.append( [ xx0-(diX_this),   yy0+(diY_this/2),  0] )  #8
        crvX=rs.AddPolyline(pt)
    elif(req==7):
        crvX=rs.AddCircle(xpt,diX)
    else:
        pt.append([xx0-diX_this, yy0-diY_this,0])
        pt.append([xx0+diX_this,yy0-diY_this,0])
        pt.append([xx0+diX_this,yy0+diY_this,0])
        pt.append([xx0-diX_this,yy0+diY_this,0])
        pt.append([xx0-diX_this,yy0-diY_this,0])
        crvX=rs.AddPolyline(pt)

    crvcen=rs.CurveAreaCentroid(crvX)[0]
    ####    offset the central curves
    diX2=diX/3.5
    diX3=diX/2.475
    diX4=diX/1.775
    crvX_off0=rs.OffsetCurve(crvX,[pt[0][0]-10000,pt[0][1],0],diX2)
    crvX_off1=rs.OffsetCurve(crvX,[pt[0][0]-10000,pt[0][1],0],diX3)
    crvX_off2=rs.OffsetCurve(crvX,[pt[0][0]-10000,pt[0][1],0],diX4)    
    
    
    #   affect subdiv curves
    temp=[]
    for i in all_subdiv_crvs:
        c=rs.AddPolyline(i)
        m=rs.CurveCurveIntersection(c,crvX_off0)
        if(m is not None):
            bx=rs.CurveBooleanDifference(c,crvX_off0)
            bool_crvs.append(bx)
            temp.append(i)
        rs.DeleteObject(c)
    for i in temp:
        all_subdiv_crvs.remove(i)
    clear_list(temp)
    
    
    temp_bx=[]#boolean curve that contains L_border curves
    for c in bool_crvs:
        if(rs.IsCurve(c)):
            m=rs.CurveCurveIntersection(c,crvX_off0)
            if(m is not None):
                bx=rs.CurveBooleanDifference(c,crvX_off0)
                temp_bx.append(bx)
                rs.DeleteObject(c)
    for i in temp_bx:
        bool_crvs.append(i)
    

    ####    cut the border_curve with crvX_off1
    ar0=rs.CurveArea(site_crv)[0]
    try:
        rs.DeleteObjects(temp1)
    except:
        pass
    temp1=[]
    k=0
    for i in new_all_border_crvs:
        ar1=rs.CurveArea(rs.coercecurve(i))[0]
        if(ar0/ar1 >16):#the smallest border
            m=rs.CurveCurveIntersection(rs.coercecurve(i),crvX_off1)
            if(m is not None):
                bx=rs.CurveBooleanDifference(rs.coercecurve(i),crvX_off1)
                temp1.append(i)
                new_all_border_crvs.insert(k,bx)
                new_all_border_crvs.remove(i)
        if(ar0/ar1 >4 and ar0/ar1 <8):#the smallest border
            m=rs.CurveCurveIntersection(rs.coercecurve(i),crvX_off2)
            if(m is not None):
                bx=rs.CurveBooleanDifference(rs.coercecurve(i),crvX_off2)
                temp1.append(i)
                new_all_border_crvs.insert(k,bx)
                new_all_border_crvs.remove(i)
        k+=1
    rs.DeleteObjects(temp1)
    rs.DeleteObjects([crvX,crvX_off1,crvX_off2])
    return crvX_off0
    pass

def modulate_line_border2(crvX):
    temp=[]
    line_borders_mod=[]    
    for i in global_line_border:
        if(rs.IsCurve(crvX) and rs.IsCurve(i)):
            m=rs.CurveCurveIntersection(i,crvX)
            if(m is not None):
                sp=rs.CurveStartPoint(i)
                ep=rs.CurveEndPoint(i)
                try:
                    p1=(m[0][1])
                    p2=(m[1][1])
                    d1=rs.Distance(sp,m[1][1])
                    d2=rs.Distance(ep,m[1][1])
                    if(d1>d2):
                        x=rs.AddLine(sp,m[1][1])
                        if(math.fabs(rs.CurveLength(x)-rs.CurveLength(i))>(rs.CurveLength(x)/10)):
                            rs.DeleteObject(x)
                            del_pt1=[sp,ep,0]
                            del_pt2=[ep,sp,0]
                            if(del_pt1 in shaped_border_crvs[1]):
                                shaped_crvs[1].remove(del_pt1)
                            if(del_pt2 in shaped_border_crvs[1]):
                                shaped_crvs[1].remove(del_pt2)
                            temp.append(i)
                    elif(d2>d1):
                        line_borders_mod.append(rs.AddLine(ep,m[0][1]))
                        x=rs.AddLine(ep,m[1][1])
                        if(math.fabs(rs.CurveLength(x)-rs.CurveLength(i))>(rs.CurveLength(x)/10)):
                            rs.DeleteObject(x)
                            del_pt1=[sp,ep,0]
                            del_pt2=[ep,sp,0]
                            if(del_pt1 in shaped_border_crvs[1]):
                                shaped_crvs[1].remove(del_pt1)
                            if(del_pt2 in shaped_border_crvs[1]):
                                shaped_crvs[1].remove(del_pt2)
                            
                except:
                    pass
    rs.DeleteObjects(temp)
    return line_borders_mod

def modulate_line_border1(crvX):
    temp=[]
    line_borders=[]
    for i in global_line_border:
        if(rs.IsCurve(crvX) and rs.IsCurve(i)):
            m=rs.CurveCurveIntersection(i,crvX)
            sp=rs.CurveStartPoint(i)
            ep=rs.CurveEndPoint(i)
            if(m is not None):
                try:
                    p1=(m[0][1])
                    p2=(m[1][1])
                    d1=rs.Distance(sp,m[0][1])
                    d2=rs.Distance(ep,m[0][1])
                    if(d1>d2):
                        x=rs.AddLine(sp,m[0][1])    
                        if(math.fabs(rs.CurveLength(x)-rs.CurveLength(i))>(rs.CurveLength(x)/10)):
                            rs.DeleteObject(x)
                            temp.append(i)
                            del_pt1=[sp,ep,0]
                            del_pt2=[ep,sp,0]
                            if(del_pt1 in shaped_border_crvs[1]):
                                shaped_crvs[1].remove(del_pt1)
                            if(del_pt2 in shaped_border_crvs[1]):
                                shaped_crvs[1].remove(del_pt2)
                        break
                    elif(d2>d1):
                        x=rs.AddLine(sp,m[0][1])    
                        if(math.fabs(rs.CurveLength(x)-rs.CurveLength(i))>(rs.CurveLength(x)/10)):
                            rs.DeleteObject(x)
                            temp.append(i)
                            del_pt1=[sp,ep,0]
                            del_pt2=[ep,sp,0]
                            if(del_pt1 in shaped_border_crvs[1]):
                                shaped_crvs[1].remove(del_pt1)
                            if(del_pt2 in shaped_border_crvs[1]):
                                shaped_crvs[1].remove(del_pt2)
                        break
                except:
                    pass
    rs.DeleteObjects(temp)
    return line_borders
    pass

def modulate_line_border3(crvX):
    temp=[]
    line_borders=[]
    for i in global_line_border:
        if(rs.IsCurve(crvX) and rs.IsCurve(i)):
            m=rs.CurveCurveIntersection(i,crvX)
            sp=rs.CurveStartPoint(i)
            ep=rs.CurveEndPoint(i)
            if(m is not None):
                try:
                    p1=(m[0][1])
                    p2=(m[1][1])
                    d1=rs.Distance(sp,m[1][1])
                    d2=rs.Distance(ep,m[1][1])
                    if(d1>d2):
                        global_line_border.append(rs.AddLine(sp,m[1][1]))
                        temp.append(i)
                        del_pt1=[sp,ep,0]
                        del_pt2=[ep,sp,0]
                        if(del_pt1 in shaped_border_crvs[1]):
                            shaped_crvs[1].remove(del_pt1)
                        if(del_pt2 in shaped_border_crvs[1]):
                            shaped_crvs[1].remove(del_pt2)
                        break
                    elif(d2>d1):
                        global_line_border.append(rs.AddLine(ep,m[1][1]))
                        temp.append(i)
                        del_pt1=[sp,ep,0]
                        del_pt2=[ep,sp,0]
                        if(del_pt1 in shaped_border_crvs[1]):
                            shaped_crvs[1].remove(del_pt1)
                        if(del_pt2 in shaped_border_crvs[1]):
                            shaped_crvs[1].remove(del_pt2)
                        break
                except:
                    pass
    rs.DeleteObjects(temp)
    return line_borders
    pass

def modulate_line_border4(crvX):
    temp=[]
    line_borders_mod=[]    
    for i in global_line_border:
        if(rs.IsCurve(crvX) and rs.IsCurve(i)):
            m=rs.CurveCurveIntersection(i,crvX)
            if(m is not None):
                sp=rs.CurveStartPoint(i)
                ep=rs.CurveEndPoint(i)
                try:
                    p1=(m[0][1])
                    p2=(m[1][1])
                    d1=rs.Distance(sp,m[0][1])
                    d2=rs.Distance(ep,m[0][1])
                    if(d1>d2):
                        line_borders_mod.append(rs.AddLine(sp,m[0][1]))
                        del_pt1=[sp,ep,0]
                        del_pt2=[ep,sp,0]
                        if(del_pt1 in shaped_border_crvs[1]):
                            shaped_crvs[1].remove(del_pt1)
                        if(del_pt2 in shaped_border_crvs[1]):
                            shaped_crvs[1].remove(del_pt2)
                        temp.append(i)
                    elif(d2>d1):
                        line_borders_mod.append(rs.AddLine(ep,m[0][1]))
                        del_pt1=[sp,ep,0]
                        del_pt2=[ep,sp,0]
                        if(del_pt1 in shaped_border_crvs[1]):
                            shaped_crvs[1].remove(del_pt1)
                        if(del_pt2 in shaped_border_crvs[1]):
                            shaped_crvs[1].remove(del_pt2)
                        temp.append(i)
                except:
                    pass
    rs.DeleteObjects(temp)
    return line_borders_mod

def draw_finalize(sender, e):
    rs.ClearCommandHistory()
    b=[]
    for i in bool_crvs:
        b.append(modulate_line_border(i))
    
    
    #rs.DeleteObjects(canal_arms)
    #rs.DeleteObjects(global_line_border)
    pass

def newRefineSystem(sender, e):
    rs.EnableRedraw(False)
    try:
        rs.DeleteObjects(shape_cross)
    except:
        pass
    try:
        rs.DeleteObjects(new_shaped_border_crvs_res_1)
    except:
        pass
    try:
        rs.DeleteObjects(new_shaped_border_crvs_res_2)
    except:
        pass
    try:
        rs.DeleteObjects(new_shaped_border_crvs_res_3)
    except:
        pass
    #check
    #from all shaped border crvs get generations based on area
    ar0=rs.CurveArea(site_crv)[0]
    try:
        for i in new_all_border_crvs:    
            ar1=rs.CurveArea(rs.coercecurve(i))[0]
            if(ar0/ar1 >4 and ar0/ar1 <8):#the middle border or highest
                new_shaped_border_crvs_res_1.append(i)
            if(ar0/ar1 >16):#the smallest border
                new_shaped_border_crvs_res_2.append(i)
    except:
        pass
    ####    IF ONLY THE SECOND EXISTS AND NOT THE THIRD  ####
    if(bor_2_yes.Checked==True and bor_3_yes.Checked==False):
        try:
            for i in bool_crvs:
                c1=rs.coercecurve(i)
                for j in new_shaped_border_crvs_res_1:#middle/highest border
                    c2=rs.coercecurve(j)
                    if(rs.IsCurve(i) and rs.IsCurve(j)):
                        m=rs.CurveCurveIntersection(i,j)
                        if(m is not None):
                            bx=rs.CurveBooleanIntersection(i,j)
                            new_shaped_border_crvs_res_3.append(bx[0])#middle/highest border
        except:
            pass
        # do the same thing for all_subdiv_crvs
        try:
            for i in all_subdiv_crvs:
                c1=rs.AddPolyline(i)
                for j in new_shaped_border_crvs_res_1:#middle/highest border
                    c2=rs.coercecurve(j)
                    if(rs.IsCurve(c1) and rs.IsCurve(j)):
                        m=rs.CurveCurveIntersection(c1,j)
                        if(m is not None):
                            bx=rs.CurveBooleanIntersection(c1,j)
                            new_shaped_border_crvs_res_3.append(bx[0])#middle/highest border
                rs.DeleteObject(c1)
        except:
            pass
        try:
            rs.DeleteObjects(new_shaped_border_crvs_res_1)
        except:
            pass
    else:
        pass
    ####    FOR ALL OTHER CASES OF THE BORDER   ####
    #from the middle borders curves, find the intersection wrt smallest border crvs
    #this cleans up the middle border crvs
    k=0
    try:
        for i in new_shaped_border_crvs_res_1:#middle/highest border
            c1=rs.coercecurve(i)
            for j in new_shaped_border_crvs_res_2:#smallest border
                c2=rs.coercecurve(j)
                if(rs.IsCurve(i) and rs.IsCurve(j)):
                    m=rs.CurveCurveIntersection(i,j)
                    if(m is not None):
                        bx=rs.CurveBooleanIntersection(i,j)
                        new_shaped_border_crvs_res_3.append(bx[0])#middle/highest border
                k+=1
    except:
        pass
    rs.DeleteObjects(new_shaped_border_crvs_res_1)
    try:
        clear_list(new_shaped_border_crvs_res_1)
    except:
        pass
    
    
    #from all boolean crvs, find the intersection between bool subdiv
    #and middle border crvs border crvs (shaped as before)
    try:
        for i in bool_crvs:
            c1=rs.coercecurve(i)
            for j in new_shaped_border_crvs_res_3:#middle/highest border
                c2=rs.coercecurve(j)
                if(rs.IsCurve(i) and rs.IsCurve(j)):
                    m=rs.CurveCurveIntersection(i,j)
                    if(m is not None):
                        bx=rs.CurveBooleanIntersection(i,j)
                        new_shaped_border_crvs_res_1.append(bx[0])#middle/highest border
    except:
        pass
    # do the same thing for all_subdiv_crvs
    try:
        for i in all_subdiv_crvs:
            c1=rs.AddPolyline(i)
            for j in new_shaped_border_crvs_res_3:#middle/highest border
                c2=rs.coercecurve(j)
                if(rs.IsCurve(c1) and rs.IsCurve(j)):
                    m=rs.CurveCurveIntersection(c1,j)
                    if(m is not None):
                        bx=rs.CurveBooleanIntersection(c1,j)
                        new_shaped_border_crvs_res_1.append(bx[0])#middle/highest border
            rs.DeleteObject(c1)
    except:
        pass
    try:
        rs.DeleteObjects(new_shaped_border_crvs_res_3)
    except:
        pass
        
    #from all boolean crvs, find intersection wrt smallest border crvs
    try:
        for i in bool_crvs:
            c1=rs.coercecurve(i)
            for j in new_shaped_border_crvs_res_2:#smallest border
                c2=rs.coercecurve(j)
                if(rs.IsCurve(i) and rs.IsCurve(j)):
                    m=rs.CurveCurveIntersection(i,j)
                    if(m is not None):
                        bx=rs.CurveBooleanIntersection(i,j)
                        new_shaped_border_crvs_res_3.append(bx[0])
    except:
        pass
    temp2=[]
    try:
        for i in all_subdiv_crvs:
            c1=rs.AddPolyline(i)
            for j in new_shaped_border_crvs_res_2:#smallest border
                c2=rs.coercecurve(j)
                if(rs.IsCurve(c1) and rs.IsCurve(j)):
                    m=rs.CurveCurveIntersection(c1,j)
                    if(m is not None):
                        bx=rs.CurveBooleanIntersection(c1,j)
                        new_shaped_border_crvs_res_3.append(bx[0])#smallest border
            rs.DeleteObject(c1)
    except:
        pass
    try:
        rs.DeleteObjects(new_shaped_border_crvs_res_2)
    except:
        pass
    rs.EnableRedraw(True)

def finalizeSystem(sender, e):
    try:
        rs.DeleteObject(shape_cross)
    except:
        pass
    try:
        rs.DeleteObject(canal_arrows)
    except:
        pass
    try:
        rs.DeleteObjects(site_labels)
    except:
        pass
    try:
        rs.DeleteObjects(anno_hatch)
    except:
        pass
    if(hatch_fig_yes.Checked==True):
        sysHatch()

def sysHatch():
    rs.EnableRedraw(False)
    print("1:"+str(len(new_shaped_border_crvs_res_1)))

    for c in new_shaped_border_crvs_res_1:
        #x=rs.AddHatch(c,'Plus',.5)
        x=rs.AddPlanarSrf(c)        
        rs.ObjectColor(x,(100,255,100))
        anno_hatch.append(x)
        
    for i in new_shaped_border_crvs_res_3:
        if(rs.IsCurve(i)):
            c=rs.AddPolyline(rs.CurvePoints(i))
            #x=rs.AddHatch(c,'Plus',.5)
            x=rs.AddPlanarSrf(c)        
            rs.ObjectColor(x,(255,100,100))
            anno_hatch.append(x)
            rs.DeleteObject(c)
    """
    print("2:"+str(len(new_shaped_border_crvs_res_2)))
    for i in new_shaped_border_crvs_res_2:
        if(rs.IsCurve(i)):
            c=rs.AddPolyline(rs.CurvePoints(i))
            rs.CopyObject(c,[2000,0,0])
            x=rs.AddHatch(c,'Plus',1)
            rs.ObjectColor(x,(255,0,0))
            anno_hatch.append(x)
    for i in new_all_border_crvs:
        if(rs.IsCurve(i)):
            c=rs.AddPolyline(rs.CurvePoints(i))
            x=rs.AddHatch(c,'Plus',1)
            rs.ObjectColor(x,(100,100,100))
            anno_hatch.append(x)
    """
    
    try:
        for i in bool_crvs:
            if(rs.IsCurve(i)):
                #x=rs.AddHatch(i,'Plus',1)
                x=rs.AddPlanarSrf(i)        
                rs.ObjectColor(x,(0,0,255))
                anno_hatch.append(x)
                pass
    except:
        pass
    try:
        for i in all_subdiv_crvs:
            c=rs.AddPolyline(i)
            #x=rs.AddHatch(c,'Plus',1)
            x=rs.AddPlanarSrf(c)        
            rs.ObjectColor(x,(0,0,255))
            rs.DeleteObject(c)
            anno_hatch.append(x)
            pass
    except:
        pass
    try:
        rs.DeleteObject(t)
    except:
        pass
    try:
        rs.DeleteObject(sx)
    except:
        pass
    t=[]
    sx=rs.CopyObject(site_crv)
    t.append(sx)
    for i in final_canal_sys:
        if(rs.IsCurve(i)):
            t.append(i)
    #x_1=rs.AddHatch(t,'Plus',1.5)
    x_1=rs.AddPlanarSrf(t)        
    rs.ObjectColor(x_1,(100,100,100))
    anno_hatch.append(x_1)
    rs.EnableRedraw(True)

def draw_clear(sender, e):
    geo1=100
    geo2=100
    geo3=100
    try:
        rs.DeleteObjects(anno_hatch)
    except:
        pass
    try:
        rs.DeleteObjects(shape_cross)
    except:
        pass
    try:
        rs.DeleteObjects(site_labels)
    except:
        pass
    try:
        rs.DeleteObjects(canal_arrows)
    except:
        pass
    #cir=[]
    try:
        rs.DeleteObjects(stage1_dummy_canal_arms)
    except:
        pass
    try:
        for i in cir:
            cir.remove(i)
    except:
        pass
    
    #bool_crvs=[]
    try:
        rs.DeleteObjects(bool_crvs)
    except:
        pass
    ####################    SUBDIV #######################
    #temp_del_list_subdiv=[]
    try:
        rs.DeleteObjects(temp_del_list_subdiv)
    except:
        pass
        
    #temp_del_list_gen=[]
    try:
        rs.DeleteObjects(temp_del_list_gen)
    except:
        pass
    
    #temp_del_list_gen_crvs=[]
    try:
        rs.DeleteObjects(temp_del_list_gen_crvs)
    except:
        pass
    
    #temp_del_list_gen_ini_crvs=[]
    try:
        rs.DeleteObjects(temp_del_list_gen_ini_crvs)
        clear_list(temp_del_list_gen_ini_crvs)
    except:
        pass
    
    #all_subdiv_crvs=[]
    try:
        clear_list(all_subdiv_crvs)
    except:
        pass
    
    #gen_crvs=[]
    try:
        clear_list(gen_crvs)
    except:
        pass
        
    #n_crv=[]
    try:
        clear_list(n_crv)
    except:
        pass
    
    #crv_gen_0=[] #   initial generation curves
    try:
        clear_list(crv_gen)
    except:
        pass
    
    #crv_gen_1=[] #   first generation curves
    try:
        clear_list(crv_gen_1)
    except:
        pass
    
    #crv_gen_2=[] #   second generation curves
    try:
        clear_list(crv_gen_2)
    except:
        pass
    
    #crv_gen_3=[] #   second generation curves
    try:
        clear_list(crv_gen_3)
    except:
        pass
    ###################     BORDER      ##################
    #all_border_crv_pts=[]
    try:
        clear_list(all_border_crv_pts)
    except:
        pass
        
    #crv_bor_0=[] #  initial border curve
    try:
        clear_list(crv_bor)
    except:
        pass
    try:
        rs.DeleteObjects(new_all_border_crvs)
    except:
        pass
    try:
        rs.DeleteObjects(new_shaped_border_crvs_res_1)
    except:
        pass
    try:
        rs.DeleteObjects(new_shaped_border_crvs_res_2)
    except:
        pass
    try:
        rs.DeleteObjects(new_shaped_border_crvs_res_3)
    except:
        pass    
    #crv_bor_1=[] #  first border curve
    try:
        clear_list(crv_bor)
    except:
        pass
    
    #crv_bor_2=[] #  second border curve
    try:
        clear_list(crv_bor_2)
    except:
        pass
    
    #temp_del_list_line_border=[]
    try:
        rs.DeleteObjects(temp_del_list_line_border)
    except:
        pass
    
    #temp_del_list_L_border=[]
    try:
        rs.DeleteObjects(temp_del_list_L_border)
        clear_list(temp_del_list_L_border)
    except:
        pass
    #str_subdiv_ratio=[]
    try:
        clear_list(str_subdiv_ratio)
    except:
        pass
    
    #str_border_ratio=[]
    try:
        clear_list(str_border_ratio)
    except:
        pass
    
    #temp_del_list_border=[]
    try:
        rs.DeleteObjects(temp_del_list_border)
    except:
        pass
        
    #temp_del_list_border_line=[]
    try:
        rs.DeleteObjects(temp_del_list_border_line)
    except:
        pass
    #dummy_border_curves=[]
    try:
        rs.DeleteObjects(dummy_border_crvs)
        clear_list(dummy_border_crvs)
    except:
        pass
    ####################################################
    
    #dummy_canal_arm_pts=[]
    try:
        clear_list(dummy_canal_arm_pts)
    except:
        pass
        
    #dummy_canal_arm_pts=[]
    try:
        rs.DeleteObjects(temp_del_canal_arms)
    except:
        pass
    
    #dummy_canal_pl_pts=[]
    try:
        clear_list(dummy_canal_pl_pts)
    except:
        pass
    
    #dummy_canal_pl_crvs=[]
    try:
        rs.DeleteObjects(dummy_canal_pl_crvs)
    except:
        pass
    
    #canal_arms=[]
    try:
        rs.DeleteObjects(canal_arms)
        clear_list(canal_arms)
    except:
        pass
    
    #canal_cen_pts=[]
    try:
        clear_list(canal_cen_pts)
    except:
        pass
    #shaped_border_crvs=[]
    try:
        clear_list(shaped_border_crvs)
        rs.DeleteObjects(shape_border_crvs)
    except:
        pass
    
    #border_crvs=[]
    try:
        clear_list(border_crvs)
        rs.DeleteObjects(border_crvs)
    except:
        pass
        
    #L_border_crvs=[]
    try:
        clear_list(L_border_crvs)
        rs.DeleteObjects(L_border_crvs)
    except:
        pass
    
    #line_border_crvs=[]
    try:
        clear_list(line_border_crvs)
        rs.DeleteObjects(line_border_crvs)
    except:
        pass
    
    #global_line_border=[]
    try:
        rs.DeleteObjects(global_line_border)
        clear_list(global_line_border)
    except:
        pass
    
    #canal_pl=[]
    try:
        rs.DeleteObjects(canal_pl)
        clear_list(canal_pl)
    except:
        pass
    
    #canal_pl_offset=[]
    try:
        rs.DeleteObjects(canal_pl_offset)
        clear_list(canal_pl_offset)
    except:
        pass
    
    #final_canal_sys=[]
    try:
        rs.DeleteObjects(final_canal_sys)
    except:
        pass
    
    #user_indent_points=[]
    try:
        rs.DeleteObjects(user_indent_points)
    except:
        pass
    
    #canal_pl=[]
    try:
        rs.DeleteObjects(canal_pl)
        clear_list(canal_pl)
    except:
        pass
        
    #canal_pl_pts=[]
    try:
        clear_list(canal_pl_pts)
    except:
        pass
        
    #def0_canal_arm=[]
    try:
        clear_list(def0_canal_arm)
    except:
        pass
    
    #dummy_res_pts=[]
    try:
        clear_list(dummy_res_pts)
    except:
        pass
    
    #dummy_canal_arms=[]
    try:
        rs.DeleteObjects(dummy_canal_arms)
        clear_list(dummy_canal_arms)
    except:
        pass
    #dummy_canal_pl_off_crvs=[]
    try:
        rs.DeleteObjects(dummy_canal_pl_off_crvs)
    except:
        pass
    #dummy_canal_pl_off_pts=[]
    try:
        clear_list(dummy_canal_pl_off_pts)
    except:
        pass
        
    #tmp0_indent=[]
    try:
        rs.DeleteObjects(tmp0_indent)
    except:
        pass
        
    #def_canal_arms=[]
    try:
        rs.DeleteObjects(def_canal_arms)
        clear_list(def_canal_arms)
    except:
        pass
        #del_crv=[]   #   tracks array ini curves in draw
    try:
        clear_list(del_crv)
    except:
        pass
    
    #del_crvs=[]  #   tracks array in subdiv
    try:
        clear_list(del_crvs)
    except:
        pass
    
    #del_pts_index=[]
    try:
        del_pts_index
    except:
        pass
    ###     last function - clean up    ###
    
    # line_borders_mod=[]
    try:
        rs.DeleteObjects(line_border_mod)
    except:
        pass
    #global_line_border=[]
    try:
        rs.DeleteObjects(global_line_border)
    except:
        pass
    #det_canal_ends=[]
    try:
        rs.DeleteObjects(det_canal_ends)
    except:
        passs

####    END OF FUNCTIONS    ####
site_dim_a=500
site_dim_b=500
p0=[0,0,0]
p1=[site_dim_a,0,0]
p2=[site_dim_a,site_dim_b,0]
p3=[0,site_dim_b,0]
site_crv=rs.AddPolyline([p0,p1,p2,p3,p0])
#site_crv=rs.GetObject("Pick Site curve")
crvcen_system=rs.CurveAreaCentroid(site_crv)[0]


ui=Nirvik_UI_Utility.UIForm("Mughal Grammar (saha/economou)")

####        Initialize       ####
ui.panel.addSeparator("",350,False)
ui.panel.addLabel("", "STAGE I", (255,0,0), False)
ui.panel.addSeparator("",350,True)
ui.panel.addLabel("","INITIALIZE",(0,0,255), True)
#ui.panel.addLabel("", "", None, True)
ui.panel.addLabel("", "initialize ratio", None, False)
subdiv_ratio1=ui.panel.addTrackBar("",850,900,50,100,50,890,300,False,None)
ui.panel.addLabel("","Construct",None, False)
ui.panel.addButton("subdiv", "Initialize System", 300, True, draw_initialize)
#ui.panel.addSeparator("",610,True)
####        subdiv system       ####

ui.panel.addLabel("","SUB DIVISION RATIO ",(0,0,255), True)
ui.panel.addLabel("", "subdiv ratio 2", None, False)
subdiv_ratio2=ui.panel.addTrackBar("",850,900,50,100,50,890,300,False,None)
#ui.panel.addLabel("", "subdiv ratio 3", None, False)
#subdiv_ratio3=ui.panel.addTrackBar("",850,950,50,100,50,900,300,False,None)
ui.panel.addLabel("", "Construct", None, False)
ui.panel.addButton("subdiv", "0. Develop Sub-Division", 300, True, draw_subdiv)

####        border system       ####
#ui.panel.addSeparator("",610,True)
ui.panel.addLabel("", "BORDER RATIO", (0,0,255), False)
#ui.panel.addLabel("", "", None, True) #NOT STINY/MITCHELL
#ui.panel.addLabel("", "border gen 1", None, False) #NOT STINY/MITCHELL
#bor_1=ui.panel.addTrackBar("", 1, 1000, 0.5, 1, 50, 875, 300, False, None) #NOT STINY/MITCHELL
bor_1_yes=ui.panel.addCheckBox("", "Border 1 - (Dummy / NOT in original grammar) ", False, False, None)
bor_2_yes=ui.panel.addCheckBox("", "Border 2", True, False, None)
bor_3_yes=ui.panel.addCheckBox("", "Border 3", True, True, None)
ui.panel.addLabel("", "Border Ratio", None, False)
ui_border_ratio=ui.panel.addTrackBar("", 875, 900, 25, 50, 25, 885, 300, False, None)
#ui.panel.addLabel("", "border gen 2", None, False)
#bor_3=ui.panel.addTrackBar("", 800, 900, 0.5, 1, 50, 850, 300, False, None)
ui.panel.addLabel("","Construct",None, False)
ui.panel.addButton("border", "1. Develop  Borders", 300, True, draw_border)

####        canal system    ####
ui.panel.addLabel("", "CANAL ARM SYSTEM", (0,0,255), False)
can_1_yes=ui.panel.addCheckBox("", "Canal 1", True, False, None)
can_2_yes=ui.panel.addCheckBox("", "Canal 2", True, False, None)
can_3_yes=ui.panel.addCheckBox("", "Canal 3", False, False, None)
ui.panel.addLabel("","Construct",None, False)
ui.panel.addButton("", "2. Canal System", 300, True, draw_canal_stage1)


##############################################################
####                     STAGE 2                          ####
##############################################################

####        canal ARM system       ####
ui.panel.addLabel("","",None,True)
ui.panel.addSeparator("",350,False)
ui.panel.addLabel("", "STAGE II", (255,0,0), False)
ui.panel.addSeparator("",350,True)

ui.panel.addLabel("", "CANAL ARM SYSTEM", (0,0,255), False)
ui.panel.addLabel("","",None,True)
ui.panel.addLabel("", "arm 1 width", None, False)
can_arm_1=ui.panel.addTrackBar("", 15, 20, 0.5, 1, 0.5, 17, 300, False, None)
ui.panel.addLabel("", "arm 2 width", None, False)
can_arm_2=ui.panel.addTrackBar("", 10, 15, 0.5, 1, 0.5, 12, 300, True, None)
ui.panel.addLabel("", "arm 3 width", None, False)
can_arm_3=ui.panel.addTrackBar("", 7, 10, 0.5, 1, 0.5, 8.5, 300, False, None)
ui.panel.addLabel("", "Construct", None, False)
ui.panel.addButton("", "3. Construct Canal Arms", 300, True, draw_canal_arms_init)

####        canal CENTER system       ####
ui.panel.addLabel("", "RESERVOIR MOTIF SYSTEM", (0,0,255), True)
ui.panel.addLabel("", "canal gen 1", None, False)
can_1_sq=ui.panel.addCheckBox("", "Square", False, False, None)
can_1_oct=ui.panel.addCheckBox("", "Octagon", True, False, None)
ui.panel.addSeparator("",15,False)
ui.panel.addLabel("", "canal gen 2", None, False)
can_2_sq=ui.panel.addCheckBox("", "Square", True, False, None)
can_2_oct=ui.panel.addCheckBox("", "Octagon", False, False, None)
ui.panel.addSeparator("",15,False)
ui.panel.addLabel("", "canal gen 3", None, False)
can_3_sq=ui.panel.addCheckBox("", "Square", False, False, None)
can_3_oct=ui.panel.addCheckBox("", "Octagon", False, True, None)
ui.panel.addLabel("","",None,True)
ui.panel.addLabel("", "Reservoir Scale Coefficient", None, False)
res_ratio=ui.panel.addTrackBar("", 40, 41, 5, 10, 5, 50, 200, False, None)
ui.panel.addLabel("", "Construct", None, False)
ui.panel.addButton("", "4. Construct Motif", 300, True, draw_reservoir_init)
#.panel.addLabel("","",None,True)


####        Articulate canal system       ####
ui.panel.addLabel("", "ARTICUALATE CCANAL END DETAILS", (0,0,255), False)
can_det_hor=ui.panel.addCheckBox("", "Hor. Axis", True, False, None)
can_det_ver=ui.panel.addCheckBox("", "Ver. Axis", True, False, None)
ui.panel.addLabel("", "Construct", None, False)
ui.panel.addButton("", "5. Develop Canal End Details", 250, True, draw_canal_ends)

##############################################################
####                     STAGE 3                          ####
##############################################################

ui.panel.addLabel("","",None,True)
ui.panel.addSeparator("",350,False)
ui.panel.addLabel("", "STAGE III", (255,0,0), False)
ui.panel.addSeparator("",350,True)
ui.panel.addLabel("","",None,True)
ui.panel.addLabel("", "REFINE BORDER SYSTEM", (0,0,255), False)
ui.panel.addLabel("","(Constrain border shapes wrt Formations)",None,False)
ui.panel.addLabel("", "Construct", None, False)
ui.panel.addButton("", "6. Develop Refinement",240, True, newRefineSystem)
ui.panel.addLabel("","",None,True)

##############################################################
####                     STAGE 3                          ####
##############################################################

####       refine border system        ####
ui.panel.addLabel("","",None,True)
ui.panel.addSeparator("",350,False)
ui.panel.addLabel("", "STAGE IV", (255,0,0), False)
ui.panel.addSeparator("",350,True)
ui.panel.addLabel("","",None,True)
ui.panel.addLabel("", "FINALIZE SYSTEM", (0,0,255), False)
ui.panel.addLabel("", "(Remove Labels / Annotation)",None,False)
hatch_fig_yes=ui.panel.addCheckBox("", "Color Figure", False, False, None)
ui.panel.addLabel("", "Construct", None, False)
ui.panel.addButton("", "7. Finalize Drawing",250, True, finalizeSystem)
ui.panel.addLabel("","",None,True)

ui.panel.addLabel("","",None,True)
ui.panel.addLabel("", "CLEAR ALL", (0,0,255), False)
ui.panel.addLabel("", " Reset & try new formations", None, False)
ui.panel.addButton("", "Clear drawing", 500, True, draw_clear)


ui.panel.addLabel("","",None,True)
ui.panel.addSeparator("",350,False)
ui.panel.addLabel("", "THANK YOU", (155,155,0), False)
ui.panel.addSeparator("",350,True)
ui.panel.addLabel("", "", None, True)
ui.layoutControls()

Rhino.UI.Dialogs.ShowSemiModal(ui)