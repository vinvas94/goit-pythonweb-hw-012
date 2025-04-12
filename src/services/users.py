from sqlalchemy.ext.asyncio import AsyncSession
from libgravatar import Gravatar

from src.database.models import User
from src.repository.users import UserRepository
from src.schemas import UserCreate


class UserService:
    def __init__(self, db: AsyncSession):
        """
        Initializes the service for working with users.

        Arguments:
            db: The asynchronous database session object.
        """
        # Initialize the repository for working with users
        self.repository = UserRepository(db)

    async def create_user(self, body: UserCreate) -> User:
        """
        Creates a new user.

        Creates an avatar for the user using Gravatar, then creates
        the user in the database.

        Arguments:
            body: User data to create a new record.

        Returns:
            User: The created user.
        """
        # Create an avatar using Gravatar
        avatar = None
        try:
            g = Gravatar(body.email)
            avatar = g.get_image()
        except Exception as e:
            # Log an error if there was a problem with Gravatar
            print(e)

        # Create the user in the database via the repository
        return await self.repository.create_user(body, avatar)

    async def get_user_by_id(self, user_id: int) -> User | None:
        """
        Retrieves a user by ID.

        Arguments:
            user_id: The user's ID.

        Returns:
            User or None: The found user or None if the user was not found.
        """
        # Retrieve the user by ID
        return await self.repository.get_user_by_id(user_id)

    async def get_user_by_username(self, username: str) -> User | None:
        """
        Retrieves a user by username.

        Arguments:
            username: The username.

        Returns:
            User or None: The found user or None if the user was not found.
        """
        # Retrieve the user by username
        return await self.repository.get_user_by_username(username)

    async def get_user_by_email(self, email: str) -> User | None:
        """
        Retrieves a user by email.

        Arguments:
            email: The user's email address.

        Returns:
            User or None: The found user or None if the user was not found.
        """
        # Retrieve the user by email
        return await self.repository.get_user_by_email(email)

    async def confirmed_email(self, email: str) -> None:
        """
        Confirms the user's email.

        Arguments:
            email: The user's email address.

        Returns:
            None
        """
        # Confirm the user's email
        return await self.repository.confirmed_email(email)

    async def update_avatar_url(self, email: str, url: str) -> User:
        """
        Updates the user's avatar URL.

        Arguments:
            email: The user's email address.
            url: The new URL for the avatar.

        Returns:
            User: The updated user.
        """
        # Update the user's avatar URL
        return await self.repository.update_avatar_url(email, url)

    async def reset_password(self, user_id: int, password: str) -> User:
        """
        Resets the user's password.

        Arguments:
            user_id: The user's ID.
            password: The new password for the user.

        Returns:
            User: The updated user.
        """
        # Reset the user's password
        return await self.repository.reset_password(user_id, password)
