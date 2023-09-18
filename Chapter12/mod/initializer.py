# mainループ中で利用する変数を大域化
from .initialize.pginit import screen, font, fontS, key

# idxの中身を定義
from .initialize.idx import Idx

# 色の定義
from .initialize.color import *

# 画像の読み込み
from .initialize.image import *

# 効果音の読み込み
from .initialize.sound import se

# 変数の宣言
from .initialize.var import *

# 共用メソッドの読み込み
from .initialize.commethod import *
