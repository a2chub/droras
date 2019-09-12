


rm  public/index.html
cp -r dist/* public
wget "https://script.google.com/macros/s/AKfycbwY05MtkIet6Yc_MlQvD9Ng4H_ZTpBcFZvtTj_BPE008Az8H8x2/exec?getrace=now" -O public/pilots.json
firebase deploy
