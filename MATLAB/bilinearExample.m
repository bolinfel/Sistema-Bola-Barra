fc = 20;

[z,p,k] = ellip(6,5,90,2*pi*fc,"s");

[num,den] = zp2tf(z,p,k);
[h,w] = freqs(num,den,1024);

plot(w/(2*pi),mag2db(abs(h)))
xline(fc,Color=[0.8500 0.3250 0.0980])

axis([0 100 -125 5])
grid
legend(["Magnitude response" "Cutoff frequency"])
xlabel("Frequency (Hz)")
ylabel("Magnitude (dB)")

fs = 200;
fp = 20;

[zd,pd,kd] = bilinear(z,p,k,fs,fp);

[hd,fd] = freqz(zp2sos(zd,pd,kd),[],fs);

plot(fd,mag2db(abs(hd)))
xline(fc,Color=[0.8500 0.3250 0.0980])

axis([0 100 -125 5])
grid
legend(["Magnitude response" "Cutoff frequency"])
xlabel("Frequency (Hz)")
ylabel("Magnitude (dB)")
