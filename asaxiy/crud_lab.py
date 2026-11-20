from sqlmodel import Session, select

from .crud import (
    kategoriya_yaratish, mahsulot_yaratish, mahsulot_olish,
    mahsulotlar_royxati, buyurtma_ber,
)
from .database import make_engine
from .models import Mijoz
from .schemas import KategoriyaKirish, MahsulotKirish

engine = make_engine()
with Session(engine) as session:
    kategoriya = kategoriya_yaratish(
        session, KategoriyaKirish(nomi="Uyga vazifa daftari")
    )
    mahsulot = mahsulot_yaratish(session, MahsulotKirish(
        kategoriya_id=kategoriya.id,
        nomi="Uyga vazifa daftari",
        narxi=10000,
        ombor_qoldigi=5,
    ))
    print("CREATE:", mahsulot.id, mahsulot.narxi)
    print("READ:", mahsulot_olish(session, mahsulot.id).nomi)
    print("LIST:", len(mahsulotlar_royxati(session, kategoriya.id)))

    mijoz = session.exec(
        select(Mijoz).where(Mijoz.telefon == "+998900000001")
    ).first()

    if mijoz is None:
        mijoz = Mijoz(
            ism="Ali",
            familiya="Valiyev",
            telefon="+998900000001",
            manzil="Toshkent",
        )
        session.add(mijoz)
        session.commit()
        session.refresh(mijoz)
    # Биринчи буюртма: 3 дона
    birinchi = buyurtma_ber(session, mijoz.id, mahsulot.id, 3)
    print("1-buyurtma:", birinchi.umumiy_summa)
    print("Qoldiq:", mahsulot_olish(session, mahsulot.id).ombor_qoldigi)

    # Иккинчи уриниш: 4 дона қолмагани учун хатони ушлаймиз
    try:
        buyurtma_ber(session, mijoz.id, mahsulot.id, 4)
    except ValueError as xato:
        print("Kutilgan xato:", xato)

    # Учинчи буюртма: қолган 2 дона
    uchinchi = buyurtma_ber(session, mijoz.id, mahsulot.id, 2)
    print("3-buyurtma:", uchinchi.umumiy_summa)
    print("Yakuniy qoldiq:", mahsulot_olish(session, mahsulot.id).ombor_qoldigi)