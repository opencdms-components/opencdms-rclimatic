from io import BytesIO
import logging
import os
import base64
import PIL.Image as Image
import rpy2.robjects as ro
from rpy2.rinterface_lib.callbacks import logger as rpy2_logger
from rpy2.robjects import pandas2ri
from rpy2.robjects.conversion import localconverter


def windrose(obs):
    # Display errors from R, but not warnings
    rpy2_logger.setLevel(logging.ERROR)

    r = ro.r

    script = os.path.join(
        os.path.dirname(__file__),
        'windrose.r',
    )

    # r(f"""source({script}""")

    with localconverter(ro.default_converter + pandas2ri.converter):
        _obs = ro.conversion.py2rpy(obs)

    # _windrose = ro.globalenv['windrose']
    # r(_windrose(_obs, 'station code', 'station name'))
    ro.globalenv['observations'] = _obs

    r(f"""
    library('magick')

    windrose <- function(data, code='', name='', uni='m/s', maxnsc=8, fnum=4, fint=5, flab=2, col=rainbow(10,.5,.92,start=.33,end=.2), ang=3*pi/16, margin=c(0,0,4,0)) {{
      z <- range(data[,1])
      startdate <- as.Date(z[1]); enddate <- as.Date(z[2])
      dd <- data[,2]; vv <- data[,3]; rm(data)
      dd[dd<0 | dd>360] <- NA
      vv[is.na(dd)] <- NA
      nd <- sum(!is.na(vv))
      if(nd==0) stop('No data available for that station and dates')
      cal <- sum(vv==0,na.rm=TRUE)
      dd <- round(dd/360*16+1); dd[dd==17] <- 1
      vm <- tapply(vv,as.factor(dd),mean,na.rm=TRUE)
      vx <- tapply(vv,as.factor(dd),max,na.rm=TRUE)
      vmt <- mean(vv,na.rm=TRUE)
      vmx <- max(vv,na.rm=TRUE)
      vv[vv==0] <- NA
      dd[is.na(vv)] <- NA
      vvc <- pretty(vv)
      nvvc <- length(vvc)-1

      if(nvvc>maxnsc) {{
        nvvc <- maxnsc
        vvf <- cut(vv,c(vvc[1:maxnsc],999))
        spclasses <- paste(vvc[1:nvvc],vvc[2:(nvvc+1)],sep='-')
        if(latex) spclasses[nvvc] <- paste('>=',vvc[maxnsc])
        else spclasses[nvvc] <- paste('>=',vvc[maxnsc])
        geflag <- TRUE
      }} else {{
        vvf <- cut(vv,vvc)
        spclasses <- paste(vvc[1:nvvc],vvc[2:(nvvc+1)],sep='-')
        geflag <- FALSE
      }}

      fr <- table(vvf,dd)

      z <- as.integer(colnames(fr))
      if(length(z)<16) {{
        zrn <- rownames(fr)
        zm <- matrix(rep(0,16*nrow(fr)),dim(fr))
        zm[,z] <- fr
        fr <- zm
        colnames(fr) <- as.character(1:16)
        rownames(fr) <- zrn
      }}

      nd1 <- sum(fr[1,]); fr[1,] <- fr[1,] * (nd1+cal)/nd1
      if(nd>0) fr <- fr*100./nd
      frt <- apply(fr,1,sum)
      frtd <- apply(fr,2,sum)
      tab <- cbind(fr,frt)
      tab <- round(rbind(tab,c(frtd,sum(frtd))),1)
      tab <- data.frame(rbind(tab,round(c(vm,vmt),1),round(c(vx,vmx),1)))
      names(tab) <- c('N','NNE','NE','ENE','E','ESE','SE','SSE','S','SSW','SW',
        'WSW','W','WNW','NW','NNW','Total')
      row.names(tab) <- c(spclasses,'Total','Mean Sp.','Mx.M.Sp.')
      old.par <- par(no.readonly = TRUE)
      on.exit(par(old.par))
      fr <- tab[1:nvvc,1:16]
      if(geflag) row.names(fr)[nvvc] <- paste('>=',vvc[nvvc])
      ndir <- 16
      nr <- nvvc
      fmax <- fnum*fint
      key <- (nr>1)

      if(key) mlf <- 3 else mlf <- 1
      par(mar=margin, new=FALSE)
      fx <- cos(pi/2-(2*pi/ndir*0:(ndir-1)))
      fy <- sin(pi/2-(2*pi/ndir*0:(ndir-1)))
      plot(fx,fy,xlim=c(-fmax-mlf*fint,fmax+fint),ylim=c(-fmax-fint,fmax+fint),
        xaxt="n",yaxt="n",xlab="",ylab="",bty="n",asp=1,type="n")
      if(nr==1) {{
        cx <- fx*fr
        cy <- fy*fr
      }}
      else {{
        f <- apply(fr,2,sum)
        cx <- fx*f
        cy <- fy*f
        for(i in nr:2) {{
          f <- f-fr[i,]
          cx <- c(cx,NA,fx*f)
          cy <- c(cy,NA,fy*f)
        }}
      }}
      polygon(cx,cy,col=col[nr:1])
      symbols(c(0*1:fnum),c(0*1:fnum),circles=c(fint*1:fnum),inches=FALSE,add=TRUE)
      segments(0*1:ndir,0*1:ndir,fmax*fx,fmax*fy)
      fmaxi <- fmax+fint/4
      text(0,fmaxi,"N")
      text(0,-fmaxi,"S")
      text(fmaxi,0,"E")
      text(-fmaxi,0,"W")
      if(flab==2)
        for(i in 1:fnum) text(i*fint*cos(ang),i*fint*sin(ang),paste(i*fint,"%"))
      else if(flab==1)
        text(fmax*cos(ang),fmax*sin(ang),paste(fmax,"%"))
      if(key) {{
        legend(-fmaxi-2.3*fint,fmaxi+2,fill=col,legend=spclasses)
        text(-fmaxi-1.5*fint,fmaxi+.9*fint,uni)
      }}
      title(paste(name,'windrose',startdate,'to',enddate))
      invisible(tab)
    }}
    figure <- image_graph(width = 350, height = 350, res = 96)

    data=observations
    ob_time=as.POSIXct(data$ob_time,tz='UTC')
    data=cbind(ob_time, data[,3:4])

    windrose(data,'838','Bracknell Beaufort Park')

    image <- image_write(figure, path = NULL, format = "png")

    """)
    image_data = ro.globalenv['image']
    image = Image.open(BytesIO(bytes(image_data)))
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    bas64_bytes = base64.b64decode(buffered.getvalue())
    print(bas64_bytes)
    return str(bas64_bytes)
