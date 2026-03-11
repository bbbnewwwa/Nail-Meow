def create_booking(db: Session, booking: schemas.BookingCreate):
    """Создать новую запись"""
    try:
        print(f"📝 Создание записи: {booking.dict()}")
        
        from datetime import datetime
        appointment_date = datetime.fromisoformat(booking.appointment_date)
        
        # Создаём запись БЕЗ master_name!
        db_booking = models.Booking(
            client_name=booking.client_name,
            client_phone=booking.client_phone,
            service_id=booking.service_id,
            appointment_date=appointment_date,
            status=booking.status or "pending",
            comment=booking.comment
        )
        
        db.add(db_booking)
        db.commit()
        db.refresh(db_booking)
        print(f"✅ Запись создана: {db_booking.id}")
        return db_booking
        
    except Exception as e:
        print(f"❌ Ошибка при создании записи: {e}")
        db.rollback()
        raise