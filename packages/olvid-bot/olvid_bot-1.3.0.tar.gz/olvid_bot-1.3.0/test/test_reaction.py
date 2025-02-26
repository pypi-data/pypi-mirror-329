import logging

from ClientHolder import ClientHolder, ClientWrapper
from olvid import datatypes, listeners
from olvid.internal import notifications
from utils import send_message_wait_and_check_content


# noinspection PyProtectedMember,DuplicatedCode
async def first_routine(client_1: ClientWrapper, client_2: ClientWrapper):
	# send a message to react to
	sent_message, received_message = await send_message_wait_and_check_content(client_1, client_2, "Message to react to")

	####
	# Add reaction
	####
	ideal_reaction_added_notif_1 = notifications.MessageReactionAddedNotification(message=sent_message._clone(), reaction=datatypes.MessageReaction(contact_id=0, reaction="A"))
	ideal_reaction_added_notif_1.message.reactions = [ideal_reaction_added_notif_1.reaction]
	ideal_reaction_added_notif_2 = notifications.MessageReactionAddedNotification(message=received_message._clone(), reaction=datatypes.MessageReaction(contact_id=received_message.sender_id, reaction="A"))
	ideal_reaction_added_notif_2.message.reactions = [ideal_reaction_added_notif_2.reaction]
	bot_1 = client_1.create_notification_bot(listeners.GenericNotificationListener(notification_type=listeners.NOTIFICATIONS.MESSAGE_REACTION_ADDED, handler=client_1.get_check_content_handler(ideal_reaction_added_notif_1), count=1))
	bot_2 = client_2.create_notification_bot(listeners.GenericNotificationListener(notification_type=listeners.NOTIFICATIONS.MESSAGE_REACTION_ADDED, handler=client_2.get_check_content_handler(ideal_reaction_added_notif_2), count=1))

	await client_1.message_react(sent_message.id, "A")
	await bot_1.wait_for_listeners_end()
	await bot_2.wait_for_listeners_end()

	####
	# Update reaction (1)
	####
	ideal_reaction_updated_notif_1 = notifications.MessageReactionUpdatedNotification(message=sent_message._clone(), reaction=datatypes.MessageReaction(contact_id=0, reaction="B"), previous_reaction=datatypes.MessageReaction(contact_id=0, reaction="A"))
	ideal_reaction_updated_notif_1.message.reactions = [ideal_reaction_updated_notif_1.reaction]
	ideal_reaction_updated_notif_2 = notifications.MessageReactionUpdatedNotification(message=received_message._clone(), reaction=datatypes.MessageReaction(contact_id=0, reaction="B"), previous_reaction=datatypes.MessageReaction(contact_id=0, reaction="A"))
	ideal_reaction_updated_notif_2.message.reactions = [ideal_reaction_updated_notif_2.reaction]
	bot_1 = client_1.create_notification_bot(listeners.GenericNotificationListener(notification_type=listeners.NOTIFICATIONS.MESSAGE_REACTION_UPDATED, handler=client_1.get_check_content_handler(ideal_reaction_updated_notif_1), count=1))
	bot_2 = client_2.create_notification_bot(listeners.GenericNotificationListener(notification_type=listeners.NOTIFICATIONS.MESSAGE_REACTION_UPDATED, handler=client_2.get_check_content_handler(ideal_reaction_updated_notif_2), count=1))

	await client_1.message_react(sent_message.id, "B")
	await bot_1.wait_for_listeners_end()
	await bot_2.wait_for_listeners_end()

	####
	# Update reaction (2)
	####
	ideal_reaction_updated_notif_1 = notifications.MessageReactionUpdatedNotification(message=sent_message._clone(), reaction=datatypes.MessageReaction(contact_id=0, reaction="C"), previous_reaction=datatypes.MessageReaction(contact_id=0, reaction="B"))
	ideal_reaction_updated_notif_1.message.reactions = [ideal_reaction_updated_notif_1.reaction]
	ideal_reaction_updated_notif_2 = notifications.MessageReactionUpdatedNotification(message=received_message._clone(), reaction=datatypes.MessageReaction(contact_id=0, reaction="C"), previous_reaction=datatypes.MessageReaction(contact_id=0, reaction="B"))
	ideal_reaction_updated_notif_2.message.reactions = [ideal_reaction_updated_notif_2.reaction]
	bot_1 = client_1.create_notification_bot(listeners.GenericNotificationListener(notification_type=listeners.NOTIFICATIONS.MESSAGE_REACTION_UPDATED, handler=client_1.get_check_content_handler(ideal_reaction_updated_notif_1), count=1))
	bot_2 = client_2.create_notification_bot(listeners.GenericNotificationListener(notification_type=listeners.NOTIFICATIONS.MESSAGE_REACTION_UPDATED, handler=client_2.get_check_content_handler(ideal_reaction_updated_notif_2), count=1))

	await client_1.message_react(sent_message.id, "C")
	await bot_1.wait_for_listeners_end()
	await bot_2.wait_for_listeners_end()

	####
	# Delete reaction
	####
	ideal_reaction_removed_notif_1 = notifications.MessageReactionRemovedNotification(message=sent_message._clone(), reaction=datatypes.MessageReaction(contact_id=0, reaction="C"))
	ideal_reaction_removed_notif_2 = notifications.MessageReactionRemovedNotification(message=received_message._clone(), reaction=datatypes.MessageReaction(contact_id=received_message.sender_id, reaction="C"))
	bot_1 = client_1.create_notification_bot(listeners.GenericNotificationListener(notification_type=listeners.NOTIFICATIONS.MESSAGE_REACTION_REMOVED, handler=client_1.get_check_content_handler(ideal_reaction_removed_notif_1), count=1))
	bot_2 = client_2.create_notification_bot(listeners.GenericNotificationListener(notification_type=listeners.NOTIFICATIONS.MESSAGE_REACTION_REMOVED, handler=client_2.get_check_content_handler(ideal_reaction_removed_notif_2), count=1))

	await client_1.message_react(sent_message.id, reaction="")

	await bot_1.wait_for_listeners_end()
	await bot_2.wait_for_listeners_end()


# noinspection PyUnusedLocal
async def test_reaction(client_holder: ClientHolder, fast_mode):
	for c1, c2 in client_holder.get_all_client_pairs():
		logging.info(f"Reaction routine: {c1.identity.id} <-> {c2.identity.id}")
		await first_routine(c1, c2)
