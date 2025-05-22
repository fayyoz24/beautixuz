from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from barber.models import Barber, WorkPost, Service, Barbershop, City, State
from faker import Faker
import random

User = get_user_model()
fake = Faker()

class Command(BaseCommand):
    help = "Create fake users, barbers, services, and work posts"

    def add_arguments(self, parser):
        parser.add_argument('--barbers', type=int, default=10, help='Number of barbers to create')
        parser.add_argument('--services', type=int, default=5, help='Number of services to create')
        parser.add_argument('--posts-per-barber', type=int, default=3, help='WorkPosts per barber')

    def handle(self, *args, **options):
        barbers_count = options['barbers']
        services_count = options['services']
        posts_per_barber = options['posts_per_barber']

        # Create Services
        services = []
        for _ in range(services_count):
            service = Service.objects.create(
                name=fake.job(),
                description=fake.sentence(),
                category=random.choice(['Haircut', 'Beard', 'Coloring']),
            )
            services.append(service)
        self.stdout.write(self.style.SUCCESS(f'✅ Created {services_count} services'))

        # Create Users & Barbers
        for i in range(barbers_count):
            while True:
                username = fake.user_name()
                if not User.objects.filter(username=username).exists():
                    break

            user = User.objects.create_user(
                username=username,
                password='password123',
                phone_number=fake.phone_number()
            )


            barbershop = Barbershop.objects.order_by('?').first()
            city_name = fake.city()
            state = fake.state()
            
            state, _ = State.objects.get_or_create(name = state)
            city, _ = City.objects.get_or_create(name=city_name, state = state)
            if not barbershop:
                barbershop = Barbershop.objects.create(
                    owner=user,
                    name=fake.company(),
                    address=fake.address(),
                    city=city,
                    state=state,
                    opening_hours={"mon": "9-18", "tue": "9-18"},
                )

            barber = Barber.objects.create(
                user=user,
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                barbershop=barbershop,
                address=fake.address(),
                city=city,
                state=state,
                bio=fake.text(),
                experience_years=random.randint(1, 15),
                instagram_handle=fake.user_name(),
                telegram_handle=fake.user_name(),
            )

            # Create WorkPosts
            for _ in range(posts_per_barber):
                WorkPost.objects.create(
                    barber=barber,
                    title=fake.catch_phrase(),
                    description=fake.text(),
                    # service=random.choice(services),
                    price=random.uniform(10, 100),
                    likes_count=random.randint(0, 50)
                )

        self.stdout.write(self.style.SUCCESS(f'🎉 Created {barbers_count} barbers and {barbers_count * posts_per_barber} work posts'))
